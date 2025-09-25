## 📘 Data Dictionary

### 🧾 Provider Model

| Field Name     | Description |
|----------------|-------------|
| `name`         | Name of the provider (e.g. company or individual) |
| `type`         | Provider type, selected from `ProviderType_CHOICES` (e.g. Internal, External) |
| `department`   | Department within the organization (optional) |
| `contact_name` | Primary contact person for the provider |
| `email`        | Contact email address |
| `phone`        | Contact phone number |
| `address`      | Street address (line 1) |
| `address2`     | Street address (line 2, optional) |
| `city`         | City of the provider |
| `county`       | County or region |
| `postcode`     | Postal code |
| `country`      | Country of operation |
| `notes`        | Internal notes or comments about the provider |
| `status`       | Operational status (e.g. Active, Inactive), from `ProviderStatus_CHOICES` |
| `website`      | Provider’s website URL (optional) |
| `industry`     | Industry classification, from `Industry_CHOICES` |
| `tags`         | Comma-separated keywords for filtering/searching (e.g. IT, Logistics) |
| `created_at`   | Timestamp when the provider record was created |
| `updated_at`   | Timestamp when the provider record was last updated |
| `created_by`   | User who created the provider record |

---

### 🧾 Service Model

| Field Name     | Description |
|----------------|-------------|
| `name`         | Name of the service offered |
| `description`  | Detailed description of the service |
| `category`     | Category or classification of the service (e.g. IT, Operations) |
| `providers`    | Many-to-many relationship to `Provider` via `ServiceProvider` |
| `notes`        | Internal notes or commentary about the service |
| `active`       | Boolean flag indicating if the service is currently active |
| `tags`         | Comma-separated keywords for filtering/searching |
| `created_at`   | Timestamp when the service record was created |
| `updated_at`   | Timestamp when the service record was last updated |
| `created_by`   | User who created the service record |

---

### 🧾 ServiceProvider Model (Join Table)

| Field Name     | Description |
|----------------|-------------|
| `service`      | Foreign key to the `Service` being provided |
| `provider`     | Foreign key to the `Provider` offering the service (`related_name='service_links'`) |
| `price`        | Price charged by the provider for this service (optional) |
| `region`       | Geographic region where the service is offered (optional) |
| `notes`        | Internal notes specific to this provider-service relationship |
| `available`    | Boolean flag indicating if the provider currently offers this service |
| `tags`         | Comma-separated keywords for filtering/searching |
| `created_at`   | Timestamp when the link was created |
| `updated_at`   | Timestamp when the link was last updated |
| `created_by`   | User who created the link between provider and service |
| `Meta.constraints` | Ensures each provider-service pair is unique (`unique_service_provider`) |