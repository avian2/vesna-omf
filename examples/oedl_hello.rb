defProperty("cluster", "unconfigured-cluster", "ID of a cluster")
defGroup("Actor", property.cluster)

onEvent(:ALL_UP) do |event|
	path = File.join(File.dirname(__FILE__), "hello.py")
	group("Actor").exec("python #{path}")
end

onEvent(:ALL_APPS_DONE) do |event|
  Experiment.done
end
