a=[['Santa_Marta', [11.08615625, -73.90399929999998]], ['Colombia', [4.11566015, -72.93168349999999]], ['Suramérica', [-19.24240005, -60.9736]], ['Estados_Unidos', [37.59999999999999, -95.665]], ['Suecia', [62.19833664999999, 17.5646052]], ['Bogotá', [4.64829755, -74.107807]], ['Cundinamarca', [4.78249555, -73.97070599999999]], ['Villavicencio', [4.110987, -73.46847245000001]], ['Australia', [-27.9210555, 133.247866]], ['Distrito_Capital', [10.48262905, -66.98021949999999]], ['Viena', [48.2206849, 16.3800599]], ['Antioquia', [7.149886049999999, -75.5033395]], ['Cartagena', [10.40014225, -75.507815]], ['Distrito_Federal_México', [19.3907336, -99.14361265000001]], ['Bucaramanga', [7.165023, -73.10824494999999]], ['Cali', [3.41059455, -76.58312205]], ['Suiza', [46.8131873, 8.22421005]], ['Popayán', [2.442695, -76.57840635]], ['Indiana', [39.7662195, -86.441277]], ['Lyon', [45.7579555, 4.835120949999999]], ['Brasil', [-14.2396023, -53.18050169999999]], ['Pasto', [1.052036, -77.20717454999999]], ['Tunja', [5.517352450000001, -73.37612444999999]], ['Aguachica', [8.24796645, -73.62394119999999]], ['Manizales', [5.0741005, -75.5028765]], ['Latinoamérica', [-11.71336855, -73.99785004999998]], ['Dinamarca', [56.15549105, 10.43308995]], ['La_Paz', [-16.52071235, -68.0915129]], ['Medellín', [6.268678, -75.596392]], ['Chile', [-36.7394323, -71.05658075000001]], ['Barranquilla', [10.9916034, -74.83900485]], ['Nigeria', [9.077751, 8.677456999999999]], ['Madrid', [40.4379543, -3.67953665]], ['Venezuela', [6.65711345, -66.61467055]], ['Francia', [46.2157467, 2.20882575]], ['Valledupar', [10.343651, -73.45780589999998]], ['Alemania', [51.16411754999999, 10.45411935]], ['Europa', [49.5, 22.0]], ['India', [21.13110835, 82.7792231]], ['Ecuador', [-1.78646385, -78.13688744999999]], ['México', [23.6266557, -102.53775015]], ['Cauca', [2.14486205, -76.98349409999999]]]

provi=[]

for i in a:

    provi+=[['<div class="info_content">'+"'+'<h3>"+ str(i[0]) +"</h3>'+"+ "'</div>"]]

print(provi)