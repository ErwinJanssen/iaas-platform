"""Unit tests for Provider Abstraction Layer."""

import pytest
from datetime import datetime

from src.providers.interface import (
    ProviderHealth,
    ProviderHealthStatus,
    ProviderType,
    VMSpec,
    VMState,
    VolumeSpec,
    VolumeState,
    VM,
    Volume,
)


class TestProviderTypes:
    """Tests for ProviderType enum."""

    def test_provider_type_values(self):
        """Test that provider types have correct values."""
        assert ProviderType.HETZNER.value == "hetzner"
        assert ProviderType.AWS.value == "aws"
        assert ProviderType.DIGITALOCEAN.value == "digitalocean"


class TestProviderHealth:
    """Tests for ProviderHealth enum."""

    def test_provider_health_values(self):
        """Test that provider health statuses have correct values."""
        assert ProviderHealth.HEALTHY.value == "healthy"
        assert ProviderHealth.DEGRADED.value == "degraded"
        assert ProviderHealth.UNHEALTHY.value == "unhealthy"
        assert ProviderHealth.UNKNOWN.value == "unknown"


class TestVMStates:
    """Tests for VMState enum."""

    def test_vm_state_values(self):
        """Test that VM states have correct values."""
        assert VMState.PENDING.value == "pending"
        assert VMState.RUNNING.value == "running"
        assert VMState.STOPPED.value == "stopped"
        assert VMState.REBOOTING.value == "rebooting"
        assert VMState.TERMINATED.value == "terminated"
        assert VMState.ERROR.value == "error"


class TestVolumeStates:
    """Tests for VolumeState enum."""

    def test_volume_state_values(self):
        """Test that volume states have correct values."""
        assert VolumeState.CREATING.value == "creating"
        assert VolumeState.AVAILABLE.value == "available"
        assert VolumeState.IN_USE.value == "in-use"
        assert VolumeState.DELETING.value == "deleting"
        assert VolumeState.ERROR.value == "error"


class TestVMSpec:
    """Tests for VMSpec model."""

    def test_vm_spec_creation(self):
        """Test creating a VM specification."""
        spec = VMSpec(
            name="test-vm",
            cpu_cores=2,
            memory_gb=4,
            image_id="ubuntu-22.04",
        )
        assert spec.name == "test-vm"
        assert spec.cpu_cores == 2
        assert spec.memory_gb == 4
        assert spec.image_id == "ubuntu-22.04"
        assert spec.ssh_keys is None
        assert spec.user_data is None
        assert spec.labels == {}

    def test_vm_spec_with_optional_fields(self):
        """Test creating a VM specification with optional fields."""
        spec = VMSpec(
            name="test-vm",
            cpu_cores=2,
            memory_gb=4,
            image_id="ubuntu-22.04",
            ssh_keys=["ssh-rsa AAAAB3NzaC1yc2E..."],
            user_data="#!/bin/bash\necho 'Hello'",
            labels={"env": "test", "team": "dev"},
        )
        assert spec.ssh_keys == ["ssh-rsa AAAAB3NzaC1yc2E..."]
        assert spec.user_data == "#!/bin/bash\necho 'Hello'"
        assert spec.labels == {"env": "test", "team": "dev"}


class TestVolumeSpec:
    """Tests for VolumeSpec model."""

    def test_volume_spec_creation(self):
        """Test creating a volume specification."""
        spec = VolumeSpec(
            name="test-volume",
            size_gb=100,
        )
        assert spec.name == "test-volume"
        assert spec.size_gb == 100
        assert spec.volume_type == "ssd"
        assert spec.labels == {}

    def test_volume_spec_with_optional_fields(self):
        """Test creating a volume specification with optional fields."""
        spec = VolumeSpec(
            name="test-volume",
            size_gb=100,
            volume_type="hdd",
            labels={"env": "test"},
        )
        assert spec.volume_type == "hdd"
        assert spec.labels == {"env": "test"}


class TestVMModel:
    """Tests for VM model."""

    def test_vm_creation(self):
        """Test creating a VM model."""
        now = datetime.now()
        vm = VM(
            id="vm-123",
            name="test-vm",
            provider_id="hcloud-456",
            provider_type=ProviderType.HETZNER,
            cpu_cores=2,
            memory_gb=4,
            image_id="ubuntu-22.04",
            state=VMState.RUNNING,
            ip_addresses=["192.168.1.1", "2001:db8::1"],
            created_at=now,
            updated_at=now,
        )
        assert vm.id == "vm-123"
        assert vm.provider_type == ProviderType.HETZNER
        assert vm.state == VMState.RUNNING
        assert vm.ip_addresses == ["192.168.1.1", "2001:db8::1"]


class TestVolumeModel:
    """Tests for Volume model."""

    def test_volume_creation(self):
        """Test creating a Volume model."""
        now = datetime.now()
        volume = Volume(
            id="vol-123",
            name="test-volume",
            provider_id="hcloud-456",
            provider_type=ProviderType.HETZNER,
            size_gb=100,
            volume_type="ssd",
            state=VolumeState.AVAILABLE,
            created_at=now,
            updated_at=now,
        )
        assert volume.id == "vol-123"
        assert volume.size_gb == 100
        assert volume.volume_type == "ssd"
        assert volume.state == VolumeState.AVAILABLE


class TestProviderHealthStatus:
    """Tests for ProviderHealthStatus model."""

    def test_health_status_creation(self):
        """Test creating a provider health status."""
        now = datetime.now()
        status = ProviderHealthStatus(
            provider_type=ProviderType.HETZNER,
            status=ProviderHealth.HEALTHY,
            last_checked=now,
            response_time_ms=123.45,
        )
        assert status.provider_type == ProviderType.HETZNER
        assert status.status == ProviderHealth.HEALTHY
        assert status.response_time_ms == 123.45

    def test_health_status_with_error(self):
        """Test creating a provider health status with error."""
        now = datetime.now()
        status = ProviderHealthStatus(
            provider_type=ProviderType.AWS,
            status=ProviderHealth.UNHEALTHY,
            last_checked=now,
            error_message="Connection timeout",
        )
        assert status.status == ProviderHealth.UNHEALTHY
        assert status.error_message == "Connection timeout"
