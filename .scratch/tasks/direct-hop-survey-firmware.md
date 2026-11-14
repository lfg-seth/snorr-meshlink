# GH-11: firmware for direct-hop vehicle surveys

Execute with GPT-6 Astra, reasoning ultra. Owner approved this scope through
grilling on 2026-11-14. Complete implementation, source/build publication and
the authorized bench acceptance autonomously; report genuine unavailable gates.

## Outcome and required inputs

Deliver RAK responder firmware and Heltec V4 GPS client firmware, plus a reusable
USB adapter/CLI test harness and exact connection documentation. A separate
parallel chat builds the GUI/webserver. Read and implement the authoritative
[v1 interface](../../docs/operations/survey-interface-v1.md) in full; it contains
the agreed packet behavior, GPS modes, settings and boundary with that worker.
Do not rebuild a GUI or webserver in this assignment.

At startup run git status. Read AGENTS.md, tracker, latest session, PROJECT.md,
CONTEXT.md and the relevant board-flashing/local-tracking rules. Consult
[source/timing evidence](../../docs/research/direct-hop-upstream-research-20261113.md)
as research, not installed feature acceptance. Owner's latest quiet/GPS choices
in the v1 interface supersede older survey drafts. Read the original checkout's
current deployment roster, station handoff and board records before hardware use.

## Scope and ownership

Owner reports three USB RAKs and one GPS Heltec V4 attached and authorizes their
reconfiguration and firmware overwrite for this task. Identify the actual four
devices by hardware/USB/!ID first; do not infer them from historical R/G numbers.
Back up each unit's own keys/profile privately and preserve recovery inputs.
Other radios, gateways, portal services and deployment sites are outside scope.

This chat alone owns those four boards/serial handles/transmitting bench. Stop
or correctly pause and verify the RAK watcher per its documented lease/heartbeat
procedure. Never contend with another process. Keep antenna requirements and
correct board image guards. A power cycle requiring human movement is an
unverified gate, not a reason to fabricate a passed check.

Create an isolated project checkout under ignored `private/worktrees/` on a
short-lived codex/ branch starting from `codex/survey-assignments`. Keep the
original shared checkout and unrelated edits intact. Initialize a separate
firmware submodule checkout rather than changing the root submodule or another
chat's SD/gateway source. Verify the actual published snorr/develop baseline
and preserve already published project behavior; do not assume the 4c96b9b
installed image equals current source. Firmware publishing remains on
snorr/develop using ordinary fast-forward history, per owner instructions.
Reconcile upstream movement before push; never force-push. Pin published source
in this repository only after build/source evidence is concrete.

Own firmware C++/target/build/tests, `scripts/survey/`, the actual USB protocol
documentation extending the v1 interface, sanitized firmware bench/release notes
and this outcome's tracker/session handoff. GUI worker owns `survey-app/` and
GUI-specific docs. Keep shared tracker/session edits small and reconcile them
at commit. You own compatible interface additions after dispatch; retain v1
names/semantics so GUI can proceed against its simulator. Publish an independent
fixed-diff firmware/security review using a subagent, then address findings.

## Implementation sequence

1. Inspect the selected baseline and document port/build/USB seams. Implement
   compact versioned PING/PONG payloads and independent request/result IDs.
   Broadcast PING identifies one target; all directly hearing nodes enter quiet,
   only target replies. Both types are never forwarded, no ACK or hidden retries,
   no MQTT acceptance. Use packet-specific uplink RSSI/SNR in pong and matching
   downlink metrics at client. Suppress generic reply/NAK storms from nontargets.
   Explicitly test malicious/incorrect positive hop budgets are not forwarded.
2. Implement fifteen-minute quiet since latest recognizable direct PING, on
   target and nontarget repeaters. The trigger is ANY recognized ping, independent
   of survey authorization. Authenticate responding separately where appropriate;
   native PKI cannot make a broadcast readable to all. Keep existing survey
   tester access policy where feasible, document the selected design and overhead.
   Audit every autonomous sender and queued-before-quiet report, smart GPS sends,
   expiry/reboot and restoration. Keep GPS acquisition/USB/pongs functional.
3. Implement the Heltec polling state machine, configurable exclusive-target
   focus plus flexible selection, adaptive scheduling and transport heartbeat.
   Maximize measured sample rate on production radio settings, allowing explicit
   recorded experimental profiles. Owner permits survey airtime to dominate the
   otherwise quiet mesh; earlier 20/40/50% traffic budgets are NOT fixed limits.
   Expose tunable utilization/backoff ceilings while retaining CAD, half-duplex,
   queue and applicable regional protections. Measure wire airtime rather than
   promising the earlier two-second estimate. Keep one outstanding attempt and
   honest timeout/retry accounting. Bound unreachable-target waiting.
4. Provide a genuinely fresh local USB GPS stream, targeting 1 Hz with configurable
   age threshold (initial 2,000 ms), no GPS RF broadcasts. Cached NodeDB polls are
   insufficient. Survey mode pauses/alerts on failure; explicit bench mode keeps
   exercising RF with missing GPS, labels it, uses null locations and records
   that outdoor location acceptance remains open. Heartbeat loss stops either
   mode; recovery requires explicit resume. Surface all faults as structured events.
5. Ship a documented, reusable Python USB adapter and a CLI/harness in
   scripts/survey/ implementing the normalized interface. It must identify
   capabilities, configure/start/stop, keep heartbeats, stream/persist attempt and
   GPS events and expose actual framing/examples to the GUI worker. Support
   Windows desktop now and Linux laptop explicitly. Use append-only private
   evidence, bounded queues and visible gaps. Keep hardware writes deliberate
   inside this authorized scope, with identity/readback/recovery checks.

## Verification and done

Build exact RAK and V4 targets; meaningful offline tests cover encoding, sequence
matching, late/duplicate packets, malformed requests, no-hop/no-ACK, target
selection, nontarget silence, quiet renewal/expiry, pending queues, GPS age/mode,
host loss and bounded overflow. Run relevant documented project check scopes.
Independent review covers routing, sender authorization, quiet suppression and
USB control/data boundaries. Fix actionable findings before acceptance.

Flash/read back the authorized boards one at a time and record each exact image,
profile, key preservation and explicit restart evidence. Keep final bench CLIENT
roles unless a temporary ROUTER test is required; restore/document temporary
changes. Prove target/nontarget behavior with all three RAKs. Test actual LoRa
receipts and traffic suppression, not just serial events. Measure baseline and
adaptive latency/rate at multiple cadences and report encoded packet sizes.
Check both direction metrics against independently observed packets where
available. Demonstrate no survey forwarding with packet captures/controlled
injection; a physical relay-only geometry that cannot be created unattended
remains a separate field gate. Never label collocated hearing as that proof.

Run a cancellable two-hour BENCH soak through a deterministic ordinary local
process, independent of model inference. Log to private files and emit compact
machine summaries/exit status. Astra waits efficiently, inspects bounded summaries
at reasonable intervals, never streams every packet through the model or loops
thinking while waiting. Keep stop/Ctrl-C effective; early cancellation yields a
partial-duration result, not a two-hour pass. Do not set up a recurring automation
to watch this job. The window-positioned Heltec should attempt real GPS; lack of
fix must not block the RF bench soak. Exercise survey GPS gating separately and
report any live-GPS limitations for the owner to repeat outdoors.

Finish with exact artifacts/checksums, source pin, per-board firmware/config
evidence, measured rates/utilization and failure/recovery results, recoverable
profiles, protocol/adapter usage examples and remaining physical/field gates.
Update relevant records once, stage explicit paths, commit/push every completed
commit to its corresponding authorized origin branch, and report failures.
Do not stop at a plan, mocks, build-only success or an unstarted soak when the
hardware/access allow completion. Final handoff names changed behavior, tests,
actual soak duration, commit/branch/publication, current serial ownership and
the precise GUI adapter entry point. Close serial handles before handing off.
