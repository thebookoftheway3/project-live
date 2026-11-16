-- SPDX-License-Identifier: AGPL-3.0-only
-- Pure feature/interaction scaffold. Caller supplies device-specific local I/O.
-- No microphone capture, BLE transfer or vendor API is installed by this module.
local Bridge = {}
Bridge.__index = Bridge
function Bridge.new()
    return setmetatable({last_time = 0, last_candidate = -math.huge, pending = false}, Bridge)
end
function Bridge:features(now, imu_candidate, acoustic_candidate, consent)
    assert(type(now) == "number" and now == now and now < math.huge and now >= self.last_time)
    self.last_time = now
    if consent ~= true then self.pending = false; return nil end
    if imu_candidate == true and acoustic_candidate == true and now - self.last_candidate >= 900 then
        self.last_candidate = now
        return "chewing_candidate" -- not confirmed ingestion; no raw audio export
    end
    return nil
end
function Bridge:prompt(authorized, local_audio)
    if authorized ~= true then return false end
    assert(type(local_audio) == "function")
    local_audio("Yes or no?") -- adapter must verify audio capability on selected device
    self.pending = true
    return true
end
function Bridge:reply(nod, explicit_no)
    if not self.pending then return nil end
    if nod == true and explicit_no ~= true then self.pending = false; return "yes" end
    if explicit_no == true and nod ~= true then self.pending = false; return "no" end
    return nil -- no motion or ambiguous motion remains unanswered
end
return Bridge
