from mininet.topo import Topo

class ProjectTopo( Topo ):
	"Simple topology used for final project."
	def __init__( self ):
		"Create custom topo."
		# Intitialize topology
		Topo.__init__( self )
		# Add hosts and switches
		h1 = self.addHost( 'h1' )
		h2 = self.addHost( 'h2' )
		h3 = self.addHost( 'h3' )
		h4 = self.addHost( 'h4' )
		centralSwitch = self.addSwitch( 's1' )

		# Add links
		# Order of parameters does not matter.
		self.addLink( h1, centralSwitch )
		self.addLink( h2, centralSwitch )
		self.addLink( h3, centralSwitch )
		self.addLink( h4, centralSwitch )

topos = { 'projecttopo' : ( lambda: PorjectTopo() ) }
