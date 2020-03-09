from mininet.topo import Topo


class FattreeTopology(Topo):
    def build(self, numEdgeSwitches=2, bw=20, hostsPerEdge=2):
        linkopts = dict(bw=bw, delay='1ms', max_queue_size=1000, loss=0, use_htb=True)
        numHosts = numEdgeSwitches * hostsPerEdge
        numCoreSwitches = numEdgeSwitches - 2
        numAggrSwitches = numEdgeSwitches

        hostIds = range(1, numHosts + 1)
        firstSwitch = max(101, numHosts + 1)
        edgeSwitchIds = range(firstSwitch, numEdgeSwitches + firstSwitch)
        aggrSwitchIds = range(numEdgeSwitches + firstSwitch, numEdgeSwitches + numAggrSwitches + firstSwitch)
        coreSwitchIds = range(numEdgeSwitches + numAggrSwitches + firstSwitch,
                              numEdgeSwitches + numAggrSwitches + firstSwitch + numCoreSwitches)

        self._coreSwitches = []
        self._aggrSwitches = []
        self._edgeSwitches = []
        self._hosts = []
        self._links = {}

        for s in coreSwitchIds:
            switch = self.addSwitch('s%s' % s, protocols='OpenFlow13')
            self._coreSwitches.append(switch)
            self._links[switch] = []

        for s in aggrSwitchIds:
            switch = self.addSwitch('s%s' % s, protocols='OpenFlow13')
            self._aggrSwitches.append(switch)
            self._links[switch] = []

        for s in edgeSwitchIds:
            switch = self.addSwitch('s%s' % s, protocols='OpenFlow13')
            self._edgeSwitches.append(switch)
            self._links[switch] = []

        # Connect the first layer of switches
        for i, s1 in enumerate(self._coreSwitches):
            for j, s2 in enumerate(self._aggrSwitches):
                self.addLink(s1, s2, **linkopts)
                self._links[s1].append(s2)
                self._links[s2].append(s1)

        # Connect the second layer of switches
        for i, s1 in enumerate(self._aggrSwitches):
            self.addLink(s1, self._edgeSwitches[i], **linkopts)
            self._links[s1].append(self._edgeSwitches[i])
            self._links[self._edgeSwitches[i]].append(s1)

            if i % 2 == 0:
                self.addLink(s1, self._edgeSwitches[i + 1], **linkopts)
                self._links[s1].append(self._edgeSwitches[i + 1])
                self._links[self._edgeSwitches[i + 1]].append(s1)
            else:
                self.addLink(s1, self._edgeSwitches[i - 1], **linkopts)
                self._links[s1].append(self._edgeSwitches[i - 1])
                self._links[self._edgeSwitches[i - 1]].append(s1)

        n = len(hostIds)
        for i, h in enumerate(hostIds):
            host = self.addHost('h%s' % h, cpu=.5/n)
            self._hosts.append(host)
            switchNum = firstSwitch + (h % numEdgeSwitches)
            switch = "s%s" % switchNum
            print('switch: {} - host:{}'.format(switch, host))
            self.addLink(switch, host, **linkopts)
            self._links[host] = [switch]
            self._links[switch].append(host)

class AbileneTopology(Topo):
    "Internet Topology Zoo Specimen."
    def addSwitch(self, name, **opts):
        kwargs = {'protocols': 'OpenFlow13'}
        kwargs.update(opts)
        return super(AbileneTopology, self).addSwitch(name, **kwargs)

    def __init__( self, **opts ):
        "Create a topology."

        # Initialize Topology
        Topo.__init__( self, **opts )

        # add nodes, switches first...
        NewYork = self.addSwitch( 's0' )
        Chicago = self.addSwitch( 's1' )
        WashingtonDC = self.addSwitch( 's2' )
        Seattle = self.addSwitch( 's3' )
        Sunnyvale = self.addSwitch( 's4' )
        LosAngeles = self.addSwitch( 's5' )
        Denver = self.addSwitch( 's6' )
        KansasCity = self.addSwitch( 's7' )
        Houston = self.addSwitch( 's8' )
        Atlanta = self.addSwitch( 's9' )
        Indianapolis = self.addSwitch( 's10' )

        # ... and now hosts
        NewYork_host = self.addHost( 'h0' )
        Chicago_host = self.addHost( 'h1' )
        WashingtonDC_host = self.addHost( 'h2' )
        Seattle_host = self.addHost( 'h3' )
        Sunnyvale_host = self.addHost( 'h4' )
        LosAngeles_host = self.addHost( 'h5' )
        Denver_host = self.addHost( 'h6' )
        KansasCity_host = self.addHost( 'h7' )
        Houston_host = self.addHost( 'h8' )
        Atlanta_host = self.addHost( 'h9' )
        Indianapolis_host = self.addHost( 'h10' )

        # add edges between switch and corresponding host
        self.addLink( NewYork , NewYork_host )
        self.addLink( Chicago , Chicago_host )
        self.addLink( WashingtonDC , WashingtonDC_host )
        self.addLink( Seattle , Seattle_host )
        self.addLink( Sunnyvale , Sunnyvale_host )
        self.addLink( LosAngeles , LosAngeles_host )
        self.addLink( Denver , Denver_host )
        self.addLink( KansasCity , KansasCity_host )
        self.addLink( Houston , Houston_host )
        self.addLink( Atlanta , Atlanta_host )
        self.addLink( Indianapolis , Indianapolis_host )

        # add edges between switches
        self.addLink( NewYork , Chicago, bw=10, delay='0.806374975652ms')
        self.addLink( NewYork , WashingtonDC, bw=10, delay='0.605826192092ms')
        self.addLink( Chicago , Indianapolis, bw=10, delay='1.34462717203ms')
        self.addLink( WashingtonDC , Atlanta, bw=10, delay='0.557636936322ms')
        self.addLink( Seattle , Sunnyvale, bw=10, delay='1.28837123738ms')
        self.addLink( Seattle , Denver, bw=10, delay='1.11169346865ms')
        self.addLink( Sunnyvale , LosAngeles, bw=10, delay='0.590813628707ms')
        self.addLink( Sunnyvale , Denver, bw=10, delay='0.997327682281ms')
        self.addLink( LosAngeles , Houston, bw=10, delay='1.20160833263ms')
        self.addLink( Denver , KansasCity, bw=10, delay='0.223328790403ms')
        self.addLink( KansasCity , Houston, bw=10, delay='1.71325092726ms')
        self.addLink( KansasCity , Indianapolis, bw=10, delay='0.240899959477ms')
        self.addLink( Houston , Atlanta, bw=10, delay='1.34344500256ms')
        self.addLink( Atlanta , Indianapolis, bw=10, delay='0.544962634977ms')

class GeantTopology(Topo):
    "Internet Topology Zoo Specimen."

    def addSwitch(self, name, **opts):
        kwargs = {'protocols': 'OpenFlow13'}
        kwargs.update(opts)
        return super(GeantTopology, self).addSwitch(name, **kwargs)

    def addLink(self, node1, node2, port1=None, port2=None,
                 key=None, **opts):
        return super(GeantTopology, self).addLink(node1, node2, **self.linkopts)

    def __init__(self, bw):
        "Create a topology."
        self.linkopts = dict(bw=bw, delay='1ms', max_queue_size=1000, loss=0, use_htb=True)

        # Initialize Topology
        Topo.__init__(self)

        # add nodes, switches first...
        ATH = self.addSwitch('s1')
        LIS = self.addSwitch('s2')
        LON = self.addSwitch('s3')
        BRU = self.addSwitch('s4')
        PAR = self.addSwitch('s5')
        DUB = self.addSwitch('s6')
        MAD = self.addSwitch('s7')
        GEN = self.addSwitch('s8')
        MIL = self.addSwitch('s9')
        SOF = self.addSwitch('s10')
        BUC = self.addSwitch('s11')
        VIE = self.addSwitch('s12')
        FRA = self.addSwitch('s13')
        COP = self.addSwitch('s14')
        TLN = self.addSwitch('s15')
        RIG = self.addSwitch('s16')
        KAU = self.addSwitch('s17')
        POZ = self.addSwitch('s18')
        PRA = self.addSwitch('s19')
        BRA = self.addSwitch('s20')
        ZAG = self.addSwitch('s21')
        LJU = self.addSwitch('s22')
        BUD = self.addSwitch('s23')
        MLT = self.addSwitch('s24')
        LUX = self.addSwitch('s25')
        MAR = self.addSwitch('s26')
        HAM = self.addSwitch('s27')
        AMS = self.addSwitch('s28')
        STO = self.addSwitch('s29')
        OSL = self.addSwitch('s30')
        HEL = self.addSwitch('s31')

        # ... and now hosts
        ATH_host = self.addHost('h1')
        LIS_host = self.addHost('h2')
        LON_host = self.addHost('h3')
        BRU_host = self.addHost('h4')
        PAR_host = self.addHost('h5')
        DUB_host = self.addHost('h6')
        MAD_host = self.addHost('h7')
        GEN_host = self.addHost('h8')
        MIL_host = self.addHost('h9')
        SOF_host = self.addHost('h10')
        BUC_host = self.addHost('h11')
        VIE_host = self.addHost('h12')
        FRA_host = self.addHost('h13')
        COP_host = self.addHost('h14')
        TLN_host = self.addHost('h15')
        RIG_host = self.addHost('h16')
        KAU_host = self.addHost('h17')
        POZ_host = self.addHost('h18')
        PRA_host = self.addHost('h19')
        BRA_host = self.addHost('h20')
        ZAG_host = self.addHost('h21')
        LJU_host = self.addHost('h22')
        BUD_host = self.addHost('h23')
        MLT_host = self.addHost('h24')
        LUX_host = self.addHost('h25')
        MAR_host = self.addHost('h26')
        HAM_host = self.addHost('h27')
        AMS_host = self.addHost('h28')
        STO_host = self.addHost('h29')
        OSL_host = self.addHost('h30')
        HEL_host = self.addHost('h31')

        # add edges between switch and corresponding host
        self.addLink(ATH, ATH_host)
        self.addLink(LIS, LIS_host)
        self.addLink(LON, LON_host)
        self.addLink(BRU, BRU_host)
        self.addLink(PAR, PAR_host)
        self.addLink(DUB, DUB_host)
        self.addLink(MAD, MAD_host)
        self.addLink(GEN, GEN_host)
        self.addLink(MIL, MIL_host)
        self.addLink(SOF, SOF_host)
        self.addLink(BUC, BUC_host)
        self.addLink(VIE, VIE_host)
        self.addLink(FRA, FRA_host)
        self.addLink(COP, COP_host)
        self.addLink(TLN, TLN_host)
        self.addLink(RIG, RIG_host)
        self.addLink(KAU, KAU_host)
        self.addLink(POZ, POZ_host)
        self.addLink(PRA, PRA_host)
        self.addLink(BRA, BRA_host)
        self.addLink(ZAG, ZAG_host)
        self.addLink(LJU, LJU_host)
        self.addLink(BUD, BUD_host)
        self.addLink(MLT, MLT_host)
        self.addLink(LUX, LUX_host)
        self.addLink(MAR, MAR_host)
        self.addLink(HAM, HAM_host)
        self.addLink(AMS, AMS_host)
        self.addLink(STO, STO_host)
        self.addLink(OSL, OSL_host)
        self.addLink(HEL, HEL_host)

        # add edges between switches
        self.addLink(ATH, MIL)
        self.addLink(MIL, ATH)
        self.addLink(MIL, VIE)
        self.addLink(MIL, MAR)
        self.addLink(MIL, GEN)
        self.addLink(GEN, MIL)
        self.addLink(MIL, MLT)
        self.addLink(GEN, FRA)
        self.addLink(FRA, GEN)
        self.addLink(GEN, PAR)
        self.addLink(PAR, GEN)
        self.addLink(GEN, PAR)
        self.addLink(FRA, POZ)
        self.addLink(GEN, MAR)
        self.addLink(MAR, MAD)
        self.addLink(MAD, PAR)
        self.addLink(MAD, LIS)
        self.addLink(LIS, LON)
        self.addLink(LON, LIS)
        self.addLink(LON, PAR)
        self.addLink(LON, DUB)
        self.addLink(DUB, LON)
        self.addLink(LON, BRU)
        self.addLink(BRU, AMS)
        self.addLink(AMS, LUX)
        self.addLink(LUX, FRA)
        self.addLink(AMS, HAM)
        self.addLink(HAM, FRA)
        self.addLink(HAM, COP)
        self.addLink(COP, AMS)
        self.addLink(FRA, POZ)
        self.addLink(FRA, PRA)
        self.addLink(FRA, BUD)
        self.addLink(FRA, VIE)
        self.addLink(POZ, PRA)
        self.addLink(POZ, KAU)
        self.addLink(KAU, RIG)
        self.addLink(ZAG, VIE)
        self.addLink(ZAG, BUD)
        self.addLink(BUD, PRA)
        self.addLink(BUD, BRA)
        self.addLink(BUD, BUC)
        self.addLink(BUD, SOF)
        self.addLink(BUD, LJU)
        self.addLink(BUC, SOF)
        self.addLink(BUC, VIE)
        self.addLink(VIE, BRA)
        self.addLink(RIG, TLN)
        self.addLink(TLN, HAM)
        self.addLink(OSL, STO)
        self.addLink(STO, HEL)
        self.addLink(STO, COP)
        self.addLink(OSL, COP)
        self.addLink(TLN, HEL)
