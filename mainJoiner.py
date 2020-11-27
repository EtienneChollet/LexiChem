import csvJoiner as cj

print('\n')

f = cj.Splits().files()

cj.Intervals().refreshAll()
for i in f:
    print(f'For {i}')
    cj.Intervals().write(i, 5)
