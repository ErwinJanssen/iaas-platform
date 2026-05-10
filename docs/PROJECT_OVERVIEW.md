# IaaS Platform - Project Overview

## Vision
Build a fully open-source Infrastructure-as-a-Service (IaaS) platform that provides virtual infrastructure provisioning and management, similar to hyperscalers like AWS, Azure, or GCP. The platform will start as a virtual provider (no physical hardware) and support multiple cloud providers with automatic failover capabilities.

## Core Principles
- **Open Source**: All components will use and prefer open-source software
- **Multi-Provider**: Support for multiple cloud providers (starting with Hetzner)
- **High Availability**: Automatic failover when a provider experiences outages
- **AI-Assisted Development**: Heavy use of AI for planning, coding, and documentation
- **Modular Design**: Components should be independently deployable and scalable

## Target Users
- Developers needing infrastructure resources
- Small to medium businesses
- DevOps teams
- Startups requiring flexible infrastructure

## Key Differentiators
1. **Provider Agnostic**: Abstract away provider-specific details
2. **Automatic Failover**: Built-in resilience across providers
3. **Open Core**: No vendor lock-in, fully transparent
4. **Developer-Friendly**: API-first design with comprehensive tooling

## Success Metrics
- [ ] Support for 3+ cloud providers
- [ ] <5 minute VM provisioning time
- [ ] 99.9% uptime for management plane
- [ ] Automatic failover within 2 minutes of provider outage
- [ ] Full API coverage for all resources
