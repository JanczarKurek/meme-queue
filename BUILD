
py_library(
    name = "resource",
    srcs = ["resource.py"],
)

py_library(
    name = "resource_provider",
    srcs = ["resource_provider.py"],
    deps = [":resource", ":resource_queue"],
)

py_library(
    name = "resource_queue",
    srcs = ["resource_queue.py"],
    deps = [":resource"],
)
