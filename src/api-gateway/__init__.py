"""API Gateway Service.

Single entry point for all user API requests to the IaaS Platform.
Handles authentication, authorization, request routing, and rate limiting.

Part of the Hybrid Architecture - uses existing tools (Crossplane, NATS, etc.)
for commodity functionality, custom logic only where necessary.
"""

__version__ = "0.1.0"
