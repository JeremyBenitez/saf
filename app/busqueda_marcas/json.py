datos = {
    "BABILON": {
      "total": 3251.5584999999946
    },
    "BARALT": {
      "total": 1568.3679999999981
    },
    "CABIMAS": {
      "total": 3450.593799999995
    },
    "CABUDARE": {
      "total": 2216.0284999999985
    },
    "CAGUA": {
      "total": 3453.151699999993
    },
    "CATIA": {
      "total": 3337.7469999999958
    },
    "CRUZ VERDE": {
      "total": 3585.0838999999946
    },
    "GUACARA": {
      "total": 3014.902599999996
    },
    "GUANARE": {
      "total": 2158.721599999999
    },
    "KAPITANA": {
      "total": 5020.985899999992
    },
    "MATURIN": {
      "total": 4886.567899999992
    },
    "PROPATRIA": {
      "total": 3970.468599999993
    },
    "UPATA": {
      "total": 3443.714999999995
    },
    "VALENCIA": {
      "total": 3602.363599999994
    },
    "VALERA": {
      "total": 2108.849299999998
    }
  }



total = []
for i in datos.values():

   total.append(i['total'])

print(sum(total))


#49069.10589999993