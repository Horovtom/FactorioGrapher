/c
local out = "["

for k, v in pairs(game.item_prototypes) do
  out = out .. "{\"name\": \"" .. v.name .. "\", \"stack_size\": " .. v.stack_size .. "},\n"
end

out = out .. "]"

game.write_file("recipes", out)
