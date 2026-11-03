param([Parameter(Mandatory=$true)][string]$DataPath)
$ErrorActionPreference='Stop'
$rootPath=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$data=Get-Content -LiteralPath $DataPath -Raw -Encoding utf8 | ConvertFrom-Json
function Html($value) { [Net.WebUtility]::HtmlEncode([string]$value) }
function UrlOk($value) { $u=$null; [Uri]::TryCreate([string]$value,[UriKind]::Absolute,[ref]$u) -and $u.Scheme -eq 'https' }
if ($data.status -ne 'approved' -or -not (UrlOk $data.socialPublishedUrl)) { throw 'Require approved ledger and confirmed published social post URL before website publication.' }
$start=[datetime]::ParseExact($data.weekStart,'yyyy-MM-dd',$null)
$end=[datetime]::ParseExact($data.weekEnd,'yyyy-MM-dd',$null)
if ($start.DayOfWeek -ne [DayOfWeek]::Sunday -or ($end-$start).Days -ne 6) { throw 'Expected a Sunday-Saturday guide.' }
$updated=[DateTimeOffset]::Parse($data.updatedAt)
if ($updated -gt [DateTimeOffset]::UtcNow.AddMinutes(5)) { throw 'Updated timestamp is in the future.' }
$items=@($data.events)
if ($items.Count -eq 0) { throw 'No verified listings: keep the unpublished/empty state; do not publish a fabricated agenda.' }
$categories=@('Networking','Workshop','Ribbon cutting','Grand opening','Professional event')
$ids=@{}
foreach ($event in $items) {
 foreach ($field in @('id','name','organizer','start','venue','address','category','whyItMatters','sourceUrl','verifiedAt')) { if ([string]::IsNullOrWhiteSpace([string]$event.$field)) { throw "Missing $field in event ledger." } }
 if ($ids.ContainsKey([string]$event.id)) { throw 'Duplicate event ID.' }; $ids[[string]$event.id]=$true
 if ($event.verificationStatus -ne 'verified' -or $event.county -ne 'Marion' -or $event.state -ne 'FL') { throw 'Only verified Marion County, Florida business events can be published.' }
 if ($event.category -notin $categories) { throw 'Unrecognized business category.' }
 if (-not (UrlOk $event.sourceUrl)) { throw 'Official HTTPS source required.' }
 if ($event.registrationUrl -and -not (UrlOk $event.registrationUrl)) { throw 'Invalid registration URL.' }
 $check=[DateTimeOffset]::Parse($event.verifiedAt)
 if ($check -gt [DateTimeOffset]::UtcNow.AddMinutes(5) -or $check -lt $updated.AddDays(-7)) { throw 'Reverify stale or future source timestamps.' }
 if ([string]$event.start -notmatch '(Z|[+-][0-9]{2}:[0-9]{2})$') { throw 'Event start needs explicit timezone offset.' }
 $when=[DateTimeOffset]::Parse($event.start)
 if ($when.Date -lt $start -or $when.Date -gt $end) { throw 'Event outside guide date range.' }
 if ($event.end) { $finish=[DateTimeOffset]::Parse($event.end); if ($finish -le $when) { throw 'Invalid event end.' } }
 if ($event.carmenAttending -eq $true -and [string]::IsNullOrWhiteSpace([string]$event.attendanceEvidence)) { throw 'Confirmed Carmen appearance needs a recorded confirmation.' }
}
# Validation completes before any website files are changed.
$cards=foreach ($event in ($items | Sort-Object { [DateTimeOffset]::Parse($_.start) })) {
 $when=[DateTimeOffset]::Parse($event.start)
 $zone=[TimeZoneInfo]::FindSystemTimeZoneById('Eastern Standard Time')
 $local=[TimeZoneInfo]::ConvertTime($when,$zone)
 $whenText=$local.ToString('dddd, MMMM d, yyyy / h:mm tt',[Globalization.CultureInfo]::GetCultureInfo('en-US'))+' Eastern'
 $cost=if ($event.costText) { Html $event.costText } else { 'Admission details: check organizer' }
 $attending=if ($event.carmenAttending -eq $true) { '<p class="status">Carmen confirmed attending</p>' } else { '' }
 $registration=if ($event.registrationUrl) { '<a class="button" href="'+(Html $event.registrationUrl)+'" rel="noopener">Registration / organizer details</a>' } else { '' }
 '<article class="event-card">'+$attending+'<p class="eyebrow">'+(Html $event.category)+'</p><h3>'+(Html $event.name)+'</h3><p class="event-meta"><time datetime="'+(Html $event.start)+'">'+(Html $whenText)+'</time><br>'+(Html $event.venue)+'<br>'+(Html $event.address)+'<br>Organizer: '+(Html $event.organizer)+'<br>'+$cost+'</p><p><strong>Your clue:</strong> '+(Html $event.whyItMatters)+'</p><div class="actions">'+$registration+'<a href="'+(Html $event.sourceUrl)+'" rel="noopener">Official source</a></div><p class="note">Details checked '+(Html $event.verifiedAt)+'. Confirm with organizer before attending.</p></article>'
}
$block='<p class="guide-date">Guide: '+$start.ToString('MMMM d')+' - '+$end.ToString('MMMM d, yyyy')+'</p><p class="note">Updated '+(Html $data.updatedAt)+'. All event times are Eastern.</p><div class="event-list">'+($cards -join [Environment]::NewLine)+'</div>'
$pagePath=Join-Path $rootPath 'where-is-carmen/index.html'
$page=[IO.File]::ReadAllText($pagePath)
if ($page -notmatch '<!-- GUIDE:START -->[\s\S]*?<!-- GUIDE:END -->') { throw 'Guide insertion markers missing.' }
$script:guideBlock=$block
$page=[regex]::Replace($page,'<!-- GUIDE:START -->[\s\S]*?<!-- GUIDE:END -->',[Text.RegularExpressions.MatchEvaluator]{ param($m) '<!-- GUIDE:START -->'+$script:guideBlock+'<!-- GUIDE:END -->' })
[IO.File]::WriteAllText($pagePath,$page,[Text.UTF8Encoding]::new($false))
Write-Output "Rendered $($items.Count) verified listings. Review the page and commit on the draft branch; this script does not deploy."
