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
