from ForcefieldTyper.GAFF.GAFFTermIter import GAFFParameterDict

gaffdict = GAFFParameterDict.fromDatFile('gaff211.dat')
with open('gaff211.settings','w+') as gaffHdler:
    for bd in gaffdict.bonds:
        settingline = ["bond_coeff\t{:5}\tharmonic\t{:5.1f}\t{:.4f}\n".format(str(bd[0]),*bd[1])]
        gaffHdler.writelines(settingline)

    for ag in gaffdict.angles:
        settingline = ["angle_coeff\t{:8}\tharmonic\t{:5.1f}\t{:6.2f}\n".format(str(ag[0]),*ag[1])]
        gaffHdler.writelines(settingline)

    for di in gaffdict.dihedrals:
        nparaSet = len(di[1])
        settingline = "dihedral_coeff\t{:11}\tfourier\t{}\t".format(di[0],nparaSet)
        for para in di[1]:
            div,Vn,gamma,n = para
            div = int(div)
            Vn = float(Vn)
            gamma = float(gamma)
            n = int(n)
            settingline += "{:6.3f}\t{:1}\t{:5.1f}\t".format(Vn/div,n,gamma)
        settingline += "\n"
        settinglines = [settingline]
        gaffHdler.writelines(settinglines)

    for im in gaffdict.impropers:
        settingline = ["improper_coeff\t{:5}\tcvff\t-1\t2\n".format(str(im[0]),im[1][0])]
        gaffHdler.writelines(settingline)
    
    for vw in gaffdict.vdw:
        settingline = ["pair_coeff\t{:2}\t{:2}\tlj/charmm/coul/long\t{:6.4f}\t{:6.4f}\n".format(str(vw[0]),str(vw[0]),vw[1][1],vw[1][0])]
        gaffHdler.writelines(settingline)