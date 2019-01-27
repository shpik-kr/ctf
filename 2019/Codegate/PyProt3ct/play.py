def op_mov_stack_integer(dict_1): # dict_1[argv0]=int(argv[1])
    int_2001=2001
    int_2002=2002
    argv0=dict_1[int_2001]
    argv0=argv0.decode("utf-8")
    argv1=dict_1[int_2002]
    argv1=argv1.decode("utf-8")
    argv1=int(argv1)
    dict_1[argv0]=argv1
    # print('dict[%s] = %d'%(argv0,argv1))
    return
def op_mov_stack_string(dict_1): # dict_1[argv0] = (argv[1])
    int_2001=2001
    int_2002=2002
    argv0=dict_1[int_2001]
    argv0=argv0.decode("utf-8")
    argv1=dict_1[int_2002]
    argv1=argv1.decode("utf-8")
    argv1=dict_1[argv1]
    dict_1[argv0]=argv1
    # print("dict[%s] = '%s'"%(argv0,argv1))
    return
def op_mov_stack_2d_dict(dict_1): # 
    OO0O00O00000O0000=2001
    O0O00O000O0O000O0=2002
    O00OO0OO00O0O000O=2003
    argv0=dict_1[OO0O00O00000O0000]
    argv0=argv0.decode("utf-8")
    argv1=dict_1[O0O00O000O0O000O0]
    argv1=argv1.decode("utf-8")
    argv1=dict_1[argv1]
    argv2=dict_1[O00OO0OO00O0O000O]
    argv2=argv2.decode("utf-8")
    if argv2.isdigit():
        argv2=int(argv2)
        # print('dict[%s] = dict[%s][%s]'%(argv0,argv1,argv2))
    else:
        argv2=dict_1[argv2]
        # print('dict[%s] = dict[%s][dict[%s]]'%(argv0,argv1,argv2))
    ptr=argv1[argv2]
    dict_1[argv0]=ptr
    return
def op_mov_stack_string_slice(dict_1):
    OO0OO0OO00O0OO0OO=2001
    OO0OO0OOO000000O0=2002
    OOOO00OOO0OO00O00=2003
    O0O0O0OO0O0O00O00=2004
    argv0=dict_1[OO0OO0OO00O0OO0OO]
    argv0=argv0.decode("utf-8")
    argv1=dict_1[OO0OO0OOO000000O0]
    argv1=argv1.decode("utf-8")
    argv2=dict_1[OOOO00OOO0OO00O00]
    argv2=argv2.decode("utf-8")
    if argv2.isdigit():
        argv2=int(argv2)
    else:
        argv2=dict_1[argv2]
    argv3=dict_1[O0O0O0OO0O0O00O00]
    argv3=argv3.decode("utf-8")
    if argv3.isdigit():
        argv3=int(argv3)
    else:
        argv3=dict_1[argv3]
    O0O0000O000O0OOOO=argv1[argv2:argv3]
    dict_1[argv0]=O0O0000O000O0OOOO
    # print('dict[%s] = "%s"[%d:%d]'%(argv0,argv1,argv2,argv3))
    return
def op_mov_2d_stack_integer(dict_1):
    O000000000000O000=2001
    O00OO00O00OO0OOO0=2002
    O00OOOOO000000000=2003
    argv0=dict_1[O000000000000O000]
    argv0=argv0.decode("utf-8")
    argv1=dict_1[O00OO00O00OO0OOO0]
    argv1=argv1.decode("utf-8")
    if argv1.isdigit():
        argv1=int(argv1)
    else:
        argv1=dict_1[argv1]
    argv2=dict_1[O00OOOOO000000000]
    argv2=argv2.decode("utf-8")
    if argv2.isdigit():
        argv2=int(argv2)
    else:
        argv2=dict_1[argv2]
    O0000OOO0OOO000O0=dict_1[argv0]
    O0000OOO0OOO000O0[argv1]=argv2
    # print('dict[%s][%d]=%d'%(argv0,argv1,argv2))
    return
def op_add(dict_1):
    OOO0O0O00OOO0O0O0=2001
    O0000000O0OOO000O=2002
    OOOOO000OOO000000=2003
    argv0=dict_1[OOO0O0O00OOO0O0O0]
    argv0=argv0.decode("utf-8")
    argv1=dict_1[O0000000O0OOO000O]
    argv1=argv1.decode("utf-8")
    if argv1.isdigit():
        argv1=int(argv1)
    else:
        argv1=dict_1[argv1]
    argv2=dict_1[OOOOO000OOO000000]
    argv2=argv2.decode("utf-8")
    if argv2.isdigit():
        argv2=int(argv2)
    else:
        argv2=dict_1[argv2]
    OOOOO0OO000OO0000=argv1+argv2
    dict_1[argv0]=OOOOO0OO000OO0000
    # print('dict[%s]=%d'%(argv0,OOOOO0OO000OO0000))
    return
def op_xor(dict_1):
    O0O000OO00OO0000O=2001
    O0OO00OOO0OO00O00=2002
    O000OOOO0OO0OO00O=2003
    argv0=dict_1[O0O000OO00OO0000O]
    argv0=argv0.decode("utf-8")
    argv1=dict_1[O0OO00OOO0OO00O00]
    argv1=argv1.decode("utf-8")
    if argv1.isdigit():
        argv1=int(argv1)
    else:
        argv1=dict_1[argv1]
    argv2=dict_1[O000OOOO0OO0OO00O]
    argv2=argv2.decode("utf-8")
    if argv2.isdigit():
        argv2=int(argv2)
    else:
        argv2=dict_1[argv2]
    OOOO0OOO0000O0000=argv1^argv2
    dict_1[argv0]=OOOO0OOO0000O0000
    # print('dict[%s]=%d'%(argv0,OOOO0OOO0000O0000))
    return
def op_and(dict_1):
    O0O0OOO00000OO00O=2001
    O0O00000O0O00OO00=2002
    OOOO0OOOOO0O00000=2003
    O0000O00OO0O0O0OO=dict_1[O0O0OOO00000OO00O]
    O0000O00OO0O0O0OO=O0000O00OO0O0O0OO.decode("utf-8")
    OO0O0O0OO00O00OO0=dict_1[O0O00000O0O00OO00]
    OO0O0O0OO00O00OO0=OO0O0O0OO00O00OO0.decode("utf-8")
    if OO0O0O0OO00O00OO0.isdigit():
        OO0O0O0OO00O00OO0=int(OO0O0O0OO00O00OO0)
    else:
        OO0O0O0OO00O00OO0=dict_1[OO0O0O0OO00O00OO0]
    O00OO000O00O0OO00=dict_1[OOOO0OOOOO0O00000]
    O00OO000O00O0OO00=O00OO000O00O0OO00.decode("utf-8")
    if O00OO000O00O0OO00.isdigit():
        O00OO000O00O0OO00=int(O00OO000O00O0OO00)
    else:
        O00OO000O00O0OO00=dict_1[O00OO000O00O0OO00]
    O000O0O00O00OOOO0=OO0O0O0OO00O00OO0&O00OO000O00O0OO00
    dict_1[O0000O00OO0O0O0OO]=O000O0O00O00OOOO0
    # print('dict[%s]=%d'%(argv0,O000O0O00O00OOOO0))
    return
def op_or(dict_1):
    O0OOOOO0O000O0O0O=2001
    O0O0OOOO000O00O0O=2002
    OO00O0OOOO00OOOO0=2003
    O0OO00OO00OOOOOO0=dict_1[O0OOOOO0O000O0O0O]
    O0OO00OO00OOOOOO0=O0OO00OO00OOOOOO0.decode("utf-8")
    O00OOO00O0000O00O=dict_1[O0O0OOOO000O00O0O]
    O00OOO00O0000O00O=O00OOO00O0000O00O.decode("utf-8")
    if O00OOO00O0000O00O.isdigit():
        O00OOO00O0000O00O=int(O00OOO00O0000O00O)
    else:
        O00OOO00O0000O00O=dict_1[O00OOO00O0000O00O]
    O0000O000000OO000=dict_1[OO00O0OOOO00OOOO0]
    O0000O000000OO000=O0000O000000OO000.decode("utf-8")
    if O0000O000000OO000.isdigit():
        O0000O000000OO000=int(O0000O000000OO000)
    else:
        O0000O000000OO000=dict_1[O0000O000000OO000]
    O0OO0OO0000000O00=O00OOO00O0000O00O|O0000O000000OO000
    dict_1[O0OO00OO00OOOOOO0]=O0OO0OO0000000O00
    # print('dict[%s]=%d'%(argv0,O0OO0OO0000000O00))
    return
def op_rshift(dict_1):
    O0OO0O000OOOOOO00=2001
    O0000O0OO00OO0000=2002
    OOOOOO00OOOO0O0O0=2003
    O0O0O0OO000O0OO0O=dict_1[O0OO0O000OOOOOO00]
    O0O0O0OO000O0OO0O=O0O0O0OO000O0OO0O.decode("utf-8")
    O0OOO0OOOOO00O0OO=dict_1[O0000O0OO00OO0000]
    O0OOO0OOOOO00O0OO=O0OOO0OOOOO00O0OO.decode("utf-8")
    if O0OOO0OOOOO00O0OO.isdigit():
        O0OOO0OOOOO00O0OO=int(O0OOO0OOOOO00O0OO)
    else:
        O0OOO0OOOOO00O0OO=dict_1[O0OOO0OOOOO00O0OO]
    O000OO00O0OOO00OO=dict_1[OOOOOO00OOOO0O0O0]
    O000OO00O0OOO00OO=O000OO00O0OOO00OO.decode("utf-8")
    if O000OO00O0OOO00OO.isdigit():
        O000OO00O0OOO00OO=int(O000OO00O0OOO00OO)
    else:
        O000OO00O0OOO00OO=dict_1[O000OO00O0OOO00OO]
    OO0OO0OOOO00O0O0O=O0OOO0OOOOO00O0OO >>O000OO00O0OOO00OO
    dict_1[O0O0O0OO000O0OO0O]=OO0OO0OOOO00O0O0O
    # print('dict[%s]=%d'%(argv0,OO0OO0OOOO00O0O0O))
    return
def op_lshift(dict_1):
    OO00O00O0O0O00OO0=2001
    OOOOOO0O0OO00OOO0=2002
    OO0O00OO0000O0O0O=2003
    O000O00O0OOOO0000=dict_1[OO00O00O0O0O00OO0]
    O000O00O0OOOO0000=O000O00O0OOOO0000.decode("utf-8")
    OOOO0OOOOO000OOOO=dict_1[OOOOOO0O0OO00OOO0]
    OOOO0OOOOO000OOOO=OOOO0OOOOO000OOOO.decode("utf-8")
    if OOOO0OOOOO000OOOO.isdigit():
        OOOO0OOOOO000OOOO=int(OOOO0OOOOO000OOOO)
    else:
        OOOO0OOOOO000OOOO=dict_1[OOOO0OOOOO000OOOO]
    OOO0OO00OO0O00OOO=dict_1[OO0O00OO0000O0O0O]
    OOO0OO00OO0O00OOO=OOO0OO00OO0O00OOO.decode("utf-8")
    if OOO0OO00OO0O00OOO.isdigit():
        OOO0OO00OO0O00OOO=int(OOO0OO00OO0O00OOO)
    else:
        OOO0OO00OO0O00OOO=dict_1[OOO0OO00OO0O00OOO]
    OO00OOOOO0OOOO0OO=OOOO0OOOOO000OOOO<<OOO0OO00OO0O00OOO
    dict_1[O000O00O0OOOO0000]=OO00OOOOO0OOOO0OO
    # print('dict[%s]=%d'%(argv0,OO00OOOOO0OOOO0OO))
    return
def op_strlen(dict_1):
    O000OO0OOO0OO0000=2001
    O0OOO0O0OO0O0OO0O=2002
    ret=1001
    OOO0OOO00O00O0OOO=dict_1[O000OO0OOO0OO0000]
    OOO0OOO00O00O0OOO=OOO0OOO00O00O0OOO.decode("utf-8")
    O0O000O00O0O0000O=dict_1[O0OOO0O0OO0O0OO0O]
    O0O000O00O0O0000O=O0O000O00O0O0000O.decode("utf-8")
    if O0O000O00O0O0000O.isdigit():
        O0O000O00O0O0000O=int(O0O000O00O0O0000O)
    else:
        O0O000O00O0O0000O=dict_1[O0O000O00O0O0000O]
    OO0OOOO000O00OOO0=eval(OOO0OOO00O00O0OOO)
    O00O0OO00000OOO0O=OO0OOOO000O00OOO0(O0O000O00O0O0000O)
    dict_1[ret]=O00O0OO00000OOO0O
    print('---------------[ Length ]---------------')
    print(O0O000O00O0O0000O)
    print('----------------------------------------')
    return
def O0O000000OO00O00O(dict_1):
    O00OO0O0O000OOO00=2001
    ret=1001
    O00O0OOOO00O00O00=dict_1[O00OO0O0O000OOO00]
    O00O0OOOO00O00O00=O00O0OOOO00O00O00.decode("utf-8")
    O00OOOO0OOO0O00OO=eval(O00O0OOOO00O00O00)
    print('---------------[ Who Are You ]---------------')
    O0O00OOO000OO0OO0=O00OOOO0OOO0O00OO()
    dict_1[ret]=O0O00OOO000OO0OO0
    return
def op_asign_ret_to_argv0(dict_1):
    OOO0OO0000OO0O0O0=2001
    ret=1001
    O00O0OO00O00OOOO0=dict_1[OOO0OO0000OO0O0O0]
    O00O0OO00O00OOOO0=O00O0OO00O00OOOO0.decode("utf-8")
    if O00O0OO00O00OOOO0.isdigit():
        O00O0OO00O00OOOO0=int(O00O0OO00O00OOOO0)
    else:
        O00O0OO00O00OOOO0=dict_1[O00O0OO00O00OOOO0]
    dict_1[ret]=O00O0OO00O00OOOO0
    # print('---------------[ Assign ]---------------')
    # print(O00O0OO00O00OOOO0)
    # print('----------------------------------------')
    return
def op_asign_argv0_to_ret(dict_1):
    O00O0000O0OO00OO0=2001
    ret=1001
    O0O0O0O0OOOOOO0OO=dict_1[O00O0000O0OO00OO0]
    O0O0O0O0OOOOOO0OO=O0O0O0O0OOOOOO0OO.decode("utf-8")
    OOOOO000OO0OOOOOO=dict_1[ret]
    dict_1[O0O0O0O0OOOOOO0OO]=OOOOO000OO0OOOOOO
    # print('---------------[ Assign ]---------------')
    # print(OOOOO000OO0OOOOOO)
    # print('----------------------------------------')
    return
def op_cmp_je(dict_1):
    OO0O00O0OOO0O0O00=2001
    OO0000000O0000OOO=2002
    O0O0OOOOOO0O00O00=2003
    int_100_pc=1000
    argv0=dict_1[OO0O00O0OOO0O0O00]
    argv0=argv0.decode("utf-8")
    argv0=int(argv0)
    OO0O00OO0O0OO0000=dict_1[OO0000000O0000OOO]
    OO0O00OO0O0OO0000=OO0O00OO0O0OO0000.decode("utf-8")
    if OO0O00OO0O0OO0000.isdigit():
        OO0O00OO0O0OO0000=int(OO0O00OO0O0OO0000)
    else:
        OO0O00OO0O0OO0000=dict_1[OO0O00OO0O0OO0000]
    OOO00OOOOO0000OO0=dict_1[O0O0OOOOOO0O00O00]
    OOO00OOOOO0000OO0=OOO00OOOOO0000OO0.decode("utf-8")
    if OOO00OOOOO0000OO0.isdigit():
        OOO00OOOOO0000OO0=int(OOO00OOOOO0000OO0)
    else:
        OOO00OOOOO0000OO0=dict_1[OOO00OOOOO0000OO0]
    if OO0O00OO0O0OO0000==OOO00OOOOO0000OO0:
        dict_1[int_100_pc]=argv0
    # print('---------------[ == ]---------------')
    # print(OO0O00OO0O0OO0000)
    # print(OOO00OOOOO0000OO0)
    # print('----------------------------------------')
    return
def op_cmp_jne(dict_1):
    OOO0OOO0OO0OO0O00=2001
    OOO000OO00O0O0O0O=2002
    O0OO000O000OOOOO0=2003
    OO00OO00OOO0OOO0O=1000
    O0O0O0OO0OOOO0O0O=dict_1[OOO0OOO0OO0OO0O00]
    O0O0O0OO0OOOO0O0O=O0O0O0OO0OOOO0O0O.decode("utf-8")
    O0O0O0OO0OOOO0O0O=int(O0O0O0OO0OOOO0O0O)
    O0OO000O0O0000O00=dict_1[OOO000OO00O0O0O0O]
    O0OO000O0O0000O00=O0OO000O0O0000O00.decode("utf-8")
    if O0OO000O0O0000O00.isdigit():
        O0OO000O0O0000O00=int(O0OO000O0O0000O00)
    else:
        O0OO000O0O0000O00=dict_1[O0OO000O0O0000O00]
    OO00O000OOO0OOO00=dict_1[O0OO000O000OOOOO0]
    OO00O000OOO0OOO00=OO00O000OOO0OOO00.decode("utf-8")
    if OO00O000OOO0OOO00.isdigit():
        OO00O000OOO0OOO00=int(OO00O000OOO0OOO00)
    else:
        OO00O000OOO0OOO00=dict_1[OO00O000OOO0OOO00]
    if O0OO000O0O0000O00 !=OO00O000OOO0OOO00:
        dict_1[OO00OO00OOO0OOO0O]=O0O0O0OO0OOOO0O0O
    # print('---------------[ != ]---------------')
    # print(OO00O000OOO0OOO00)
    # print(O0OO000O0O0000O00)
    # print('----------------------------------------')
    return
def op_cmp_jb(dict_1):
    OOO0OO0OOO0OO0O00=2001
    OO00OOOO0OOOOOOOO=2002
    OOOO00OO0OOOO00O0=2003
    OOOOO0O0OOO0OOO0O=1000
    OO0OOO0O0O0000000=dict_1[OOO0OO0OOO0OO0O00]
    OO0OOO0O0O0000000=OO0OOO0O0O0000000.decode("utf-8")
    OO0OOO0O0O0000000=int(OO0OOO0O0O0000000)
    O0OOO0O000O00OO0O=dict_1[OO00OOOO0OOOOOOOO]
    O0OOO0O000O00OO0O=O0OOO0O000O00OO0O.decode("utf-8")
    if O0OOO0O000O00OO0O.isdigit():
        O0OOO0O000O00OO0O=int(O0OOO0O000O00OO0O)
    else:
        O0OOO0O000O00OO0O=dict_1[O0OOO0O000O00OO0O]
    OOO0OOO00O0000O0O=dict_1[OOOO00OO0OOOO00O0]
    OOO0OOO00O0000O0O=OOO0OOO00O0000O0O.decode("utf-8")
    if OOO0OOO00O0000O0O.isdigit():
        OOO0OOO00O0000O0O=int(OOO0OOO00O0000O0O)
    else:
        OOO0OOO00O0000O0O=dict_1[OOO0OOO00O0000O0O]
    if O0OOO0O000O00OO0O<OOO0OOO00O0000O0O:
         dict_1[OOOOO0O0OOO0OOO0O]=OO0OOO0O0O0000000
    # print('---------------[ < ]---------------')
    # print(O0OOO0O000O00OO0O)
    # print(OOO0OOO00O0000O0O)
    # print('----------------------------------------')
    return
def op_cmp_jae(dict_1):
    O00OO0OO0OO0OO00O=2001
    O00O00O0OOO0OOO00=2002
    OO0O000O00O0000O0=2003
    OO00O0O0O00000OO0=1000
    OO000OOOO00OO0OOO=dict_1[O00OO0OO0OO0OO00O]
    OO000OOOO00OO0OOO=OO000OOOO00OO0OOO.decode("utf-8")
    OO000OOOO00OO0OOO=int(OO000OOOO00OO0OOO)
    O00000OO000OO00O0=dict_1[O00O00O0OOO0OOO00]
    O00000OO000OO00O0=O00000OO000OO00O0.decode("utf-8")
    if O00000OO000OO00O0.isdigit():
        O00000OO000OO00O0=int(O00000OO000OO00O0)
    else:
        O00000OO000OO00O0=dict_1[O00000OO000OO00O0]
    OO00OOOO00O000OOO=dict_1[OO0O000O00O0000O0]
    OO00OOOO00O000OOO=OO00OOOO00O000OOO.decode("utf-8")
    if OO00OOOO00O000OOO.isdigit():
        OO00OOOO00O000OOO=int(OO00OOOO00O000OOO)
    else:
        OO00OOOO00O000OOO=dict_1[OO00OOOO00O000OOO]
    if O00000OO000OO00O0 >=OO00OOOO00O000OOO:
        dict_1[OO00O0O0O00000OO0]=OO000OOOO00OO0OOO
    # print('---------------[ >= ]---------------')
    # print(O00000OO000OO00O0)
    # print(OO00OOOO00O000OOO)
    # print('----------------------------------------')
    return
def op_jmp(dict_1):
    O0OOOOOO0OO0O0OOO=2001
    O0O0OOOO0OOO0OO00=1000
    argv0=dict_1[O0OOOOOO0OO0O0OOO]
    argv0=argv0.decode("utf-8")
    argv0=int(argv0)
    dict_1[O0O0OOOO0OOO0OO00]=argv0

    return
def O0O0O0O00OO0O0O0O(argv0 ,argv1):
    dict_1=dict()
    int_1000=1000
    int_1001=1001
    int_2001=2001
    int_2002=2002
    int_2003=2003
    int_2004=2004
    int_0=0
    int_1=1
    int_2=2
    int_3=3
    int_4=4
    int_5=5
    dict_1[int_1000]=0
    dict_1[int_1001]=0
    dict_1["flag"]=argv1
    isFinish=0
    while isFinish==0:
        pc=dict_1[int_1000]
        op=argv0[pc]
        pc=pc+int_1
        next_op=argv0[pc]
        pc=pc+int_1
        if int_0<next_op: # argv parsing
            op_argv_length=argv0[pc]
            pc=pc+int_1
            op_argv_start_address=pc
            op_argv_end_address=pc+op_argv_length
            op_argv0=argv0[op_argv_start_address:op_argv_end_address]
            dict_1[int_2001]=op_argv0
            pc=pc+op_argv_length
        if int_1<next_op:
            op_argv_length=argv0[pc]
            pc=pc+int_1
            op_argv_start_address=pc
            op_argv_end_address=pc+op_argv_length
            op_argv0=argv0[op_argv_start_address:op_argv_end_address]
            dict_1[int_2002]=op_argv0
            pc=pc+op_argv_length
        if int_2<next_op:
            op_argv_length=argv0[pc]
            pc=pc+int_1
            op_argv_start_address=pc
            op_argv_end_address=pc+op_argv_length
            op_argv0=argv0[op_argv_start_address:op_argv_end_address]
            dict_1[int_2003]=op_argv0
            pc=pc+op_argv_length
        if int_3<next_op:
            op_argv_length=argv0[pc]
            pc=pc+int_1
            op_argv_start_address=pc
            op_argv_end_address=pc+op_argv_length
            op_argv0=argv0[op_argv_start_address:op_argv_end_address]
            dict_1[int_2004]=op_argv0
            pc=pc+op_argv_length
        dict_1[int_1000]=pc
        if op==0:
            print('mov %s,%s'%(dict_1[int_2001],dict_1[int_2002]))
            op_mov_stack_integer(dict_1)
        elif op==2:
            print('mov %s,%s'%(dict_1[int_2001],dict_1[int_2002]))
            op_mov_2d_stack_integer(dict_1)
        elif op==8:
            print('cmp %s,%s'%(dict_1[int_2002],dict_1[int_2003]))
            print('jae %s'%(dict_1[int_2001]))
            op_cmp_jae(dict_1)
        elif op==11:
            print('cmp %s,%s'%(dict_1[int_2002],dict_1[int_2003]))
            print('jmp %s'%(dict_1[int_2001]))
            op_jmp(dict_1)
        elif op==34:
            print('mov %s,%s[%s]'%(dict_1[int_2001],dict_1[int_2002],dict_1[int_2003]))
            op_mov_stack_2d_dict(dict_1)
        elif op==41:
            print('strlen(%s)'%(dict_1[int_2002]))
            op_strlen(dict_1)
        elif op==44:
            print('????')
            O0O000000OO00O00O(dict_1)
        elif op==49:
            print('cmp %s,%s'%(dict_1[int_2002],dict_1[int_2003]))
            print('jb %s'%(dict_1[int_2001]))
            op_cmp_jb(dict_1)
        elif op==72:
            print('%s = return'%(dict_1[int_2001]))
            op_asign_argv0_to_ret(dict_1)
        elif op==74:
            print('return = %s'%(dict_1[int_2001]))
            op_asign_ret_to_argv0(dict_1)
        elif op==81:
            print('cmp %s,%s'%(dict_1[int_2002],dict_1[int_2003]))
            print('je %s'%(dict_1[int_2001]))
            op_cmp_je(dict_1)
        elif op==82:
            print('mov %s,"%s"'%(dict_1[int_2001],dict_1[int_2002]))
            op_mov_stack_string(dict_1)
        elif op==91:
            print('cmp %s,%s'%(dict_1[int_2002],dict_1[int_2003]))
            print('jne %s'%(dict_1[int_2001]))
            op_cmp_jne(dict_1)
        elif op==99:
            print('mov %s,"%s"[%s:%s]'%(dict_1[int_2001],dict_1[int_2002],dict_1[int_2003],dict_1[int_2004]))
            op_mov_stack_string_slice(dict_1)
        elif op==102:
            op_add(dict_1)
            print('add %s,%s,%s'%(dict_1[int_2001],dict_1[int_2002],dict_1[int_2003]))
        elif op==111:
            op_or(dict_1)
            print('or %s,%s,%s'%(dict_1[int_2001],dict_1[int_2002],dict_1[int_2003]))
        elif op==131:
            op_and(dict_1)
            print('and %s,%s,%s'%(dict_1[int_2001],dict_1[int_2002],dict_1[int_2003]))
        elif op==151:
            op_lshift(dict_1)
            print('lshift %s,%s,%s'%(dict_1[int_2001],dict_1[int_2002],dict_1[int_2003]))
        elif op==171:
            op_rshift(dict_1)
            print('rshift %s,%s.%s'%(dict_1[int_2001],dict_1[int_2002],dict_1[int_2003]))
        elif op==186:
            op_xor(dict_1)
            print('xor %s,%s,%s'%(dict_1[int_2001],dict_1[int_2002],dict_1[int_2003]))
        pc=dict_1[int_1000]
        if op==74:
            isFinish=1
    output=dict_1[int_1001]
    # print(dict_1)
    return output
