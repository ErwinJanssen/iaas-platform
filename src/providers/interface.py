"""Provider Interface.

This module defines the abstract base class that all provider adapters must implement.
It provides a unified interface for interacting with different cloud providers.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ProviderType(str, Enum):
    """Supported provider types."""
    HETZNER = "hetzner"
    AWS = "aws"
    DIGITALOCEAN = "digitalocean"
    # Add more providers as needed


class ProviderHealth(str, Enum):
    """Provider health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class VMState(str, Enum):
    """Virtual machine states."""
    PENDING = "pending"
    RUNNING = "running"
    STOPPED = "stopped"
    REBOOTING = "rebooting"
    TERMINATED = "terminated"
    ERROR = "error"


class VolumeState(str, Enum):
    """Volume states."""
    CREATING = "creating"
    AVAILABLE = "available"
    IN_USE = "in-use"
    DELETING = "deleting"
    ERROR = "error"


# Request Models
class VMSpec(BaseModel):
    """Specification for creating a virtual machine."""
    name: str
    cpu_cores: int
    memory_gb: int
    image_id: str
    ssh_keys: Optional[List[str]] = None
    user_data: Optional[str] = None
    labels: Optional[Dict[str, str]] = None


class VolumeSpec(BaseModel):
    """Specification for creating a volume."""
    name: str
    size_gb: int
    volume_type: str = "ssd"  # ssd, hdd, etc.
    labels: Optional[Dict[str, str]] = None


# Response Models
class VM(BaseModel):
    """Virtual machine resource."""
    id: str
    name: str
    provider_id: str
    provider_type: ProviderType
    cpu_cores: int
    memory_gb: int
    image_id: str
    state: VMState
    ip_addresses: List[str]
    created_at: datetime
    updated_at: datetime
    labels: Dict[str, str] = {}


class Volume(BaseModel):
    """Volume resource."""
    id: str
    name: str
    provider_id: str
    provider_type: ProviderType
    size_gb: int
    volume_type: str
    state: VolumeState
    attached_to: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    labels: Dict[str, str] = {}


class ProviderHealthStatus(BaseModel):
    """Provider health status."""
    provider_type: ProviderType
    status: ProviderHealth
    last_checked: datetime
    response_time_ms: Optional[float] = None
    error_message: Optional[str] = None


class ProviderInterface(ABC):
    """Abstract base class for provider adapters.
    
    All provider adapters must implement this interface to ensure
    compatibility with the IaaS platform.
    """

    @property
    @abstractmethod
    def provider_type(self) -> ProviderType:
        """Get the provider type."""
        pass

    @abstractmethod
    async def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Authenticate with the provider.
        
        Args:
            credentials: Provider-specific credentials
            
        Returns:
            True if authentication succeeded, False otherwise
        """
        pass

    @abstractmethod
    async def health_check(self) -> ProviderHealthStatus:
        """Check the health of the provider.
        
        Returns:
            ProviderHealthStatus with current health information
        """
        pass

    # Virtual Machine Operations
    @abstractmethod
    async def create_vm(self, spec: VMSpec) -> VM:
        """Create a new virtual machine.
        
        Args:
            spec: VM specification
            
        Returns:
            VM resource with provider-specific ID
        """
        pass

    @abstractmethod
    async def get_vm(self, vm_id: str) -> Optional[VM]:
        """Get a virtual machine by ID.
        
        Args:
            vm_id: Platform VM ID or provider VM ID
            
        Returns:
            VM resource or None if not found
        """
        pass

    @abstractmethod
    async def list_vms(self, filters: Optional[Dict[str, Any]] = None) -> List[VM]:
        """List all virtual machines.
        
        Args:
            filters: Optional filters (e.g., {"state": "running"})
            
        Returns:
            List of VM resources
        """
        pass

    @abstractmethod
    async def start_vm(self, vm_id: str) -> bool:
        """Start a virtual machine.
        
        Args:
            vm_id: VM ID
            
        Returns:
            True if operation succeeded
        """
        pass

    @abstractmethod
    async def stop_vm(self, vm_id: str, force: bool = False) -> bool:
        """Stop a virtual machine.
        
        Args:
            vm_id: VM ID
            force: Force stop (don't wait for graceful shutdown)
            
        Returns:
            True if operation succeeded
        """
        pass

    @abstractmethod
    async def reboot_vm(self, vm_id: str, force: bool = False) -> bool:
        """Reboot a virtual machine.
        
        Args:
            vm_id: VM ID
            force: Force reboot (hard reboot)
            
        Returns:
            True if operation succeeded
        """
        pass

    @abstractmethod
    async def delete_vm(self, vm_id: str, force: bool = False) -> bool:
        """Delete a virtual machine.
        
        Args:
            vm_id: VM ID
            force: Force delete (skip confirmation)
            
        Returns:
            True if operation succeeded
        """
        pass

    # Volume Operations
    @abstractmethod
    async def create_volume(self, spec: VolumeSpec) -> Volume:
        """Create a new volume.
        
        Args:
            spec: Volume specification
            
        Returns:
            Volume resource with provider-specific ID
        """
        pass

    @abstractmethod
    async def get_volume(self, volume_id: str) -> Optional[Volume]:
        """Get a volume by ID.
        
        Args:
            volume_id: Platform volume ID or provider volume ID
            
        Returns:
            Volume resource or None if not found
        """
        pass

    @abstractmethod
    async def list_volumes(self, filters: Optional[Dict[str, Any]] = None) -> List[Volume]:
        """List all volumes.
        
        Args:
            filters: Optional filters
            
        Returns:
            List of Volume resources
        """
        pass

    @abstractmethod
    async def attach_volume(self, volume_id: str, vm_id: str) -> bool:
        """Attach a volume to a VM.
        
        Args:
            volume_id: Volume ID
            vm_id: VM ID
            
        Returns:
            True if operation succeeded
        """
        pass

    @abstractmethod
    async def detach_volume(self, volume_id: str, vm_id: str, force: bool = False) -> bool:
        """Detach a volume from a VM.
        
        Args:
            volume_id: Volume ID
            vm_id: VM ID
            force: Force detach
            
        Returns:
            True if operation succeeded
        """
        pass

    @abstractmethod
    async def delete_volume(self, volume_id: str, force: bool = False) -> bool:
        """Delete a volume.
        
        Args:
            volume_id: Volume ID
            force: Force delete
            
        Returns:
            True if operation succeeded
        """
        pass

    # Network Operations (to be implemented)
    # TODO: Add network, subnet, firewall, load balancer operations

    # Cleanup
    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up resources and connections."""
        pass
