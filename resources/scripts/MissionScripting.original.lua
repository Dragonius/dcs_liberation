--Initialization script for the Mission lua Environment (SSE)

dofile('Scripts/ScriptingSystem.lua')


dofile(lfs.writedir()..'Scripts/DCSUDPMissionDataExport.lua')

--Sanitize Mission Scripting environment
--This makes unavailable some unsecure functions.
--Mission downloaded from server to client may contain potentialy harmful lua code that may use these functions.
--You can remove the code below and make availble these functions at your own risk.

-- local function sanitizeModule(name)
-- 	_G[name] = nil
-- 	package.loaded[name] = nil
-- end
--
-- do
-- 	--sanitizeModule('os'), commented by DSMC: if you won't desanitized environment, please disable the autosave option!
-- 	--sanitizeModule('io'), commented by DSMC: if you won't desanitized environment, please disable the autosave option!
-- 	--sanitizeModule('lfs'), commented by DSMC: if you won't desanitized environment, please disable the autosave option!
-- 	require = nil
-- 	loadlib = nil
-- end
