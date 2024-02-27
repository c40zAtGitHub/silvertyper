#'X'means dummy atom

atomSymbols = ['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg',                                                                                                
           'Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','v','Cr','Mn',                                                                                         
           'Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr',                                                                                     
           'Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb',                                                                                      
           'Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd',                                                                                      
           'Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir',                                                                                      
           'Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac',                                                                                          
           'Th','Pa','U']

isotopeMasses = [{1:1.00782,2:2.0141},
{3:3.01602,4:4.0026},
{6:6.01512,7:7.016},
{9:9.01218},
{10:10.0129,11:11.0093},
{12:12.0,13:13.0033},
{14:14.003,15:15.0001},
{16:15.9949,17:16.9991,18:17.9991},
{19:18.9984},
{20:19.9924,21:20.9938,22:21.9913},
{23:22.9897},
{24:23.985,25:24.9858,26:25.9825},
{27:26.9815},
{28:27.9769,29:28.9764,30:29.9737},
{31:30.9737},
{32:31.972,33:32.9714,34:33.9678,36:35.967},
{35:34.9688,37:36.9659},
{36:35.9675,38:37.9627,40:39.9623},
{39:38.9637,40:39.9639,41:40.9618},
{40:39.9625,42:41.9586,43:42.9587,44:43.9554,46:45.9536,48:47.9525},
{45:44.9559},
{46:45.9526,47:46.9517,48:47.9479,49:48.9478,50:49.9447},
{50:49.9471,51:50.9439},
{50:49.946,52:51.9405,53:52.9406,54:53.9388},
{55:54.938},
{54:53.9396,56:55.9349,57:56.9353,58:57.9332},
{59:58.9331},
{58:57.9353,60:59.9307,61:60.931,62:61.9283,64:63.9279},
{63:62.9295,65:64.9277},
{64:63.9291,66:65.926,67:66.9271,68:67.9248,70:69.9253},
{69:68.9255,71:70.9247},
{70:69.9242,72:71.922,73:72.9234,74:73.9211,76:75.9214},
{75:74.9215},
{74:73.9224,76:75.9192,77:76.9199,78:77.9173,80:79.9165,82:81.9166},
{79:78.9183,81:80.9162},
{78:77.9203,80:79.9163,82:81.9134,83:82.9141,84:83.9114,86:85.9106},
{85:84.9117,87:86.9091},
{84:83.9134,86:85.9092,87:86.9088,88:87.9056},
{89:88.9058},
{90:89.9046,91:90.9056,92:91.905,94:93.9063,96:95.9082},
{93:92.9063},
{92:91.9068,94:93.905,95:94.9058,96:95.9046,97:96.906,98:97.9054,100:99.9074},
{97:96.9063,98:97.9072,99:98.9062},
{96:95.9075,98:97.9052,99:98.9059,100:99.9042,101:100.905,102:101.904,104:103.905},
{103:102.905},
{102:101.905,104:103.904,105:104.905,106:105.903,108:107.903,110:109.905},
{107:106.905,109:108.904},
{106:105.906,108:107.904,110:109.903,111:110.904,112:111.902,113:112.904,114:113.903,116:115.904},
{113:112.904,115:114.903},
{112:111.904,114:113.902,115:114.903,116:115.901,117:116.902,118:117.901,119:118.903,120:119.902,122:121.903,124:123.905},
{121:120.903,123:122.904},
{120:119.904,122:121.903,123:122.904,124:123.902,125:124.904,126:125.903,128:127.904,130:129.906},
{127:126.904},
{124:123.905,126:125.904,128:127.903,129:128.904,130:129.903,131:130.905,132:131.904,134:133.905,136:135.907},
{133:132.905},
{130:129.906,132:131.905,134:133.904,135:134.905,136:135.904,137:136.905,138:137.905},
{138:137.907,139:138.906},
{136:135.907,138:137.905,140:139.905,142:141.909},
{141:140.907},
{142:141.907,143:142.909,144:143.91,145:144.912,146:145.913,148:147.916,150:149.92},
{145:144.912,147:146.915},
{144:143.912,147:146.914,148:147.914,149:148.917,150:149.917,152:151.919,154:153.922},
{151:150.919,153:152.921},
{152:151.919,154:153.92,155:154.922,156:155.922,157:156.923,158:157.924,160:159.927},
{159:158.925},
{156:155.924,158:157.924,160:159.925,161:160.926,162:161.926,163:162.928,164:163.929},
{165:164.93},
{162:161.928,164:163.929,166:165.93,167:166.932,168:167.932,170:169.935},
{169:168.934},
{168:167.933,170:169.934,171:170.936,172:171.936,173:172.938,174:173.938,176:175.942},
{175:174.94,176:175.942},
{174:173.94,176:175.941,177:176.943,178:177.943,179:178.945,180:179.946},
{180:179.947,181:180.947},
{180:179.946,182:181.948,183:182.95,184:183.95,186:185.954},
{185:184.952,187:186.955},
{184:183.952,186:185.953,187:186.955,188:187.955,189:188.958,190:189.958,192:191.961},
{191:190.96,193:192.962},
{190:189.959,192:191.961,194:193.962,195:194.964,196:195.964,198:197.967},
{197:196.966},
{196:195.965,198:197.966,199:198.968,200:199.968,201:200.97,202:201.97,204:203.973},
{203:202.972,205:204.974},
{204:203.973,206:205.974,207:206.975,208:207.976},
{209:208.98},
{209:208.982,210:209.982},
{210:209.987,211:210.987},
{211:210.99,220:220.011,222:222.017},
{223:223.019},
{223:223.018,224:224.02,226:226.025,228:228.031},
{227:227.027},
{232:232.038},
{231:231.035},
{234:234.0495,235:235.0439,238:238.0508}]

defaultIsotope = [1,4,7,9,11,12,14,16,19,20,23,24,27,28,31,32,                                                                                                   
                  35,40,39,40,45,48,51,52,55,56,59,58,63,64,69,                                                                                                  
                  74,75,80,79,84,85,88,89,90,93,98,98,102,103,106,                                                                                               
                  107,114,115,120,121,130,127,132,133,138,139,140,                                                                                               
                  141,142,145,152,153,158,159,164,165,166,169,174,175,                                                                                           
                  180,181,184,187,192,193,195,197,202,205,208,209,209,                                                                                           
                  210,222,223,226,227,232,231,238]