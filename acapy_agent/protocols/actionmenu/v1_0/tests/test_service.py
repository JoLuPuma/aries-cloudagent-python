from unittest import IsolatedAsyncioTestCase, mock

from .....core.event_bus import EventBus, MockEventBus
from .....messaging.request_context import RequestContext
from .....utils.testing import create_test_profile
from .. import driver_service as test_module


class TestActionMenuService(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.profile = await create_test_profile()
        self.context = RequestContext(self.profile)

    async def test_get_active_menu(self):
        mock_event_bus = MockEventBus()
        self.context.profile.context.injector.bind_instance(EventBus, mock_event_bus)

        self.menu_service = await test_module.DriverMenuService.service_handler()(
            self.context
        )

        connection = mock.MagicMock()
        connection.connection_id = "connid"
        thread_id = "thid"

        await self.menu_service.get_active_menu(
            self.context.profile, connection, thread_id
        )

        assert len(mock_event_bus.events) == 1
        (_, event) = mock_event_bus.events[0]
        assert event.topic == "acapy::actionmenu::get-active-menu"
        assert event.payload == {
            "connection_id": connection.connection_id,
            "thread_id": thread_id,
        }

    async def test_perform_menu_action(self):
        mock_event_bus = MockEventBus()
        self.context.profile.context.injector.bind_instance(EventBus, mock_event_bus)

        self.menu_service = await test_module.DriverMenuService.service_handler()(
            self.context
        )

        action_name = "action"
        action_params = {"a": 1, "b": 2}
        connection = mock.MagicMock()
        connection.connection_id = "connid"
        thread_id = "thid"

        await self.menu_service.perform_menu_action(
            self.context.profile,
            action_name,
            action_params,
            connection,
            thread_id,
        )

        assert len(mock_event_bus.events) == 1
        (_, event) = mock_event_bus.events[0]
        assert event.topic == "acapy::actionmenu::perform-menu-action"
        assert event.payload == {
            "connection_id": connection.connection_id,
            "thread_id": thread_id,
            "action_name": action_name,
            "action_params": action_params,
        }
