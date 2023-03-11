"""Tests for iZone."""
import logging
from unittest.mock import Mock, patch

from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send
import pytest

from custom_components.izone.const import DISPATCH_CONTROLLER_DISCOVERED, IZONE

_LOGGER = logging.getLogger(__name__)

pytestmark = pytest.mark.asyncio

controllers = {}


@pytest.fixture()
def mock_disco():
    """Mock discovery service."""
    disco = Mock()
    disco.pi_disco = Mock()
    disco.pi_disco.controllers = controllers
    yield disco
    controllers.clear()


@pytest.fixture
def mock_start_discovery(mock_disco):
    def do_disovered(hass):
        async_dispatcher_send(hass, DISPATCH_CONTROLLER_DISCOVERED, True)
        return mock_disco

    yield do_disovered


async def test_not_found(hass: HomeAssistant, mock_start_discovery) -> None:
    """Test not finding iZone controller."""

    with patch(
        "custom_components.izone.discovery.async_start_discovery_service",
        side_effect=mock_start_discovery,
    ), patch(
        "custom_components.izone.discovery.async_stop_discovery_service",
        return_value=None,
    ) as stop_disco:
        result = await hass.config_entries.flow.async_init(
            IZONE, context={"source": config_entries.SOURCE_USER}
        )

        # Confirmation form
        assert result["type"] == data_entry_flow.FlowResultType.FORM

        result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
        assert result["type"] == data_entry_flow.FlowResultType.ABORT

        await hass.async_block_till_done()

    stop_disco.assert_called_once()


async def test_found(hass: HomeAssistant, mock_start_discovery) -> None:
    """Test not finding iZone controller."""
    controllers["blah"] = object()

    with patch(
        "custom_components.izone.climate.async_setup_entry",
        return_value=True,
    ), patch(
        "custom_components.izone.discovery.async_start_discovery_service",
        side_effect=mock_start_discovery,
    ), patch(
        "custom_components.izone.discovery.async_stop_discovery_service",
        return_value=None,
    ):
        result = await hass.config_entries.flow.async_init(
            IZONE, context={"source": config_entries.SOURCE_USER}
        )

        # Confirmation form
        assert result["type"] == data_entry_flow.FlowResultType.FORM

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )
        assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
