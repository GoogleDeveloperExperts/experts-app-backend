""" Endpoint api server registration."""

import endpoints
from .web_endpoints import ActivityDetailService
from .web_endpoints import ActivityMasterService
from .web_endpoints import AccountService
from .web_endpoints import ProductGroupService
from .web_endpoints import ActivityTypeService
from .web_endpoints import ActivityGroupService

application = endpoints.api_server([ActivityMasterService, ActivityDetailService,
                                    AccountService, ProductGroupService,
                                    ActivityTypeService, ActivityGroupService],
                                   restricted=False)
