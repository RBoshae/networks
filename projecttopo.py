from mininet.topo import Topo

class ProjectTopo( Topo ):
	"Simple topology used for final project."
	def __init__( self ):
		"Create custom topo."
		# Intitialize topology
		Topo.__init__( self )
		# Add hosts and switches
		b1 = self.addHost( 'b1' )
		b2 = self.addHost( 'b2' )
		b3 = self.addHost( 'b3' )
		b4 = self.addHost( 'b4' )
		centralSwitch = self.addSwitch( 's1' )

		# Add links
		# Order of parameters does not matter.
		self.addLink( b1, centralSwitch )
		self.addLink( b2, centralSwitch )
		self.addLink( b3, centralSwitch )
		self.addLink( b4, centralSwitch )

topos = { 'projecttopo' : ( lambda: ProjectTopo() ) }
