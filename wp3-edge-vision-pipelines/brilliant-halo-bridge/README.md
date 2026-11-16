# Brilliant Halo / Frame bridge

`bridge.lua` consumes synthetic IMU/acoustic candidate flags, applies a 15-minute
retrigger interval, and accepts an injected local prompt function. A pending prompt
can receive a positive nod or an explicit negative input; absent/ambiguous motion
remains unanswered. No capture, acoustic classifier, nod classifier or transport
is implemented. Prompt expiry and persistent budgets must be added to an actual
device adapter before use.

Halo and Frame have distinct [official hardware and Lua APIs](https://docs.brilliant.xyz/).
Verify the selected device's IMU, microphone and audio-output capabilities; a
bone-conduction prompt path is a requirement to investigate, not an asserted
capability of both products. No invented vendor API calls or firmware flashes are
included. Lua execution and device behavior are not yet validated.
