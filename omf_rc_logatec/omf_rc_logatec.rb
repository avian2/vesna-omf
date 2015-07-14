require 'omf_rc'
require 'omf_rc/resource_proxy/application'

module OmfRc::ResourceProxy::Cluster
	include OmfRc::ResourceProxyDSL

	register_proxy :cluster

	hook :before_create do |cluster, type, opts|
		if type == "application"
			info "Cluster #{cluster.uid} creating #{type}"
			env = opts[:environments]
			if env.nil?
				env = {}
				opts[:environments] = env
			end
			env["CLUSTER_UID"] = cluster.uid
		end
	end
end

logging = { level: {
		default: 'debug',
		'OmfCommon::Comm::AMQP::Topic' => 'info',
		'OmfRc::ResourceFactory' => 'info',
	},
	appenders: {
		stdout: {
			date_pattern: '%H:%M:%S',
			pattern: '%d %5l %c: %m\n',
			color_scheme: 'none'
		}
        }
}

OmfCommon.init(:development, communication: { url: 'amqp://localhost' }, logging: logging) do
	OmfCommon.comm.on_connected do |comm|
		info "Cluster controller >> Connected to XMPP server"

		res = []

		clusters = ['lgt01', 'lgt02']
		clusters.each do |uid|
			r = OmfRc::ResourceFactory.create(:cluster, uid: uid)
			res.push r
		end

		comm.on_interrupted do
			res.each do |r|
				r.disconnect
			end
		end
	end
end
