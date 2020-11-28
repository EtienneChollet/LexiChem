import csvJoiner as cj
import xmlScraper as xs

print('\n')
def updateDbase():
    f = cj.Splits().files()

    cj.Intervals().refreshAll()
    for i in f:
        print(f'For {i}')
        cj.Intervals().write(i, 5)


    