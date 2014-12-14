from Level import Level

try:
	failing_level = Level(1)
except:
	pass

perimeter_level = Level(1, True)
area_level = Level(1, False, True)
both_level = Level(1, True, True)

print perimeter_level.level
print area_level.level
print both_level.level
