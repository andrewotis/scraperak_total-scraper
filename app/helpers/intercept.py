async def intercept_route(route):
    """intercept all requests and abort blocked ones"""
    block_resource_types = ['beacon','csp_report','font','image','imageset','media','object','texttrack']
    block_resource_names = ['adzerk','analytics','cdn.api.twitter','doubleclick','exelator','facebook','fontawesome','google','google-analytics','googletagmanager']
    if route.request.resource_type in block_resource_types:
        return await route.abort()
    if any(key in route.request.url for key in block_resource_names):
        return await route.abort()
    return await route.continue_()