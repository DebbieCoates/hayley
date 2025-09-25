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


### 🧾 Category

| Field         | Type         | Description                          |
|---------------|--------------|--------------------------------------|
| id            | AutoField    | Primary key                          |
| name          | CharField    | Unique name of the category          |
| description   | TextField    | Optional description                 |

🔗 Relationships:
- One-to-many with `Service` (via `category`)


### Service

| Field         | Type         | Description                          |
|---------------|--------------|--------------------------------------|
| id            | AutoField    | Primary key                          |
| name          | CharField    | Name of the service                  |
| description   | TextField    | Optional description                 |
| category      | ForeignKey   | Linked to `Category`                 |
| tags          | CharField    | Comma-separated keywords             |
| active        | BooleanField | Whether the service is active        |
| created_by    | ForeignKey   | Linked to `User`                     |
| created_at    | DateTime     | Timestamp of creation                |
| updated_at    | DateTime     | Timestamp of last update             |

🔗 Relationships:
- Many-to-one with `Category`
- One-to-many with `Solution`

### Solution

| Field           | Type           | Description                          |
|-----------------|----------------|--------------------------------------|
| id              | AutoField      | Primary key                          |
| name            | CharField      | Name of the solution                 |
| description     | TextField      | Optional description                 |
| service         | ForeignKey     | Linked to `Service`                  |
| providers       | ManyToMany     | Linked to multiple `Provider`s       |
| tags            | CharField      | Comma-separated keywords             |
| budget_eligible | BooleanField   | Whether it's budget eligible         |
| created_by      | ForeignKey     | Linked to `User`                     |
| created_at      | DateTime       | Timestamp of creation                |
| updated_at      | DateTime       | Timestamp of last update             |

🔗 Relationships:
- Many-to-one with `Service`
- Many-to-many with `Provider`
- Many-to-many with `ProblemStatement` (via `ProblemSolutionLink`)


### ProblemSolutionLink

| Field         | Type         | Description                          |
|---------------|--------------|--------------------------------------|
| id            | AutoField    | Primary key                          |
| problem       | ForeignKey   | Linked to `ProblemStatement`         |
| solution      | ForeignKey   | Linked to `Solution`                 |
| notes         | TextField    | Optional notes                       |
| created_at    | DateTime     | Timestamp of creation                |
| updated_at    | DateTime     | Timestamp of last update             |

🔗 Relationships:
- Many-to-one with `ProblemStatement`
- Many-to-one with `Solution`

# 📘 Entity Relationship Diagram

## 🧍 Customer
- `id`: AutoField (PK)
- `name`: CharField
- `main_contact`: CharField
- `email`: EmailField
- `phone`: CharField
- `industry`: CharField (choices)
- `location`: CharField (choices)
- `account_manager`: CharField
- `status`: CharField (choices)
- `notes`: TextField
- `logo`: ImageField
- `archived`: BooleanField
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

🔗 **Relationships**
- 1️⃣→∞ `ProblemStatement.customer`

---

## 🧠 ProblemStatement
- `id`: AutoField (PK)
- `customer_id`: FK → Customer
- `title`: CharField
- `description`: TextField
- `impact`: TextField
- `urgency`: CharField (choices)
- `status`: CharField (choices)
- `notes`: TextField
- `archived`: BooleanField
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

🔗 **Relationships**
- ∞→1️⃣ `Customer`
- ∞→∞ `Solution` via `ProblemSolutionLink`

---

## 🏢 Provider
- `id`: AutoField (PK)
- `name`: CharField
- `type`: CharField (choices)
- `department`: CharField
- `contact_name`: CharField
- `email`: EmailField
- `phone`: CharField
- `address`: CharField
- `address2`: CharField
- `city`: CharField
- `county`: CharField
- `postcode`: CharField
- `country`: CharField
- `notes`: TextField
- `status`: CharField (choices)
- `website`: URLField
- `industry`: CharField (choices)
- `tags`: CharField
- `created_by`: FK → User
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

🔗 **Relationships**
- ∞→∞ `Solution.providers`

---

## 🗂️ Category
- `id`: AutoField (PK)
- `name`: CharField (unique)
- `description`: TextField

🔗 **Relationships**
- 1️⃣→∞ `Service.category`

---

## 🛠️ Service
- `id`: AutoField (PK)
- `name`: CharField
- `description`: TextField
- `category_id`: FK → Category
- `tags`: CharField
- `active`: BooleanField
- `created_by`: FK → User
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

🔗 **Relationships**
- ∞→1️⃣ `Category`
- 1️⃣→∞ `Solution.service`

---

## 💡 Solution
- `id`: AutoField (PK)
- `name`: CharField
- `description`: TextField
- `service_id`: FK → Service
- `tags`: CharField
- `budget_eligible`: BooleanField
- `created_by`: FK → User
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

🔗 **Relationships**
- ∞→1️⃣ `Service`
- ∞→∞ `Provider`
- ∞→∞ `ProblemStatement` via `ProblemSolutionLink`

---

## 🔗 ProblemSolutionLink
- `id`: AutoField (PK)
- `problem_id`: FK → ProblemStatement
- `solution_id`: FK → Solution
- `notes`: TextField
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

🔗 **Relationships**
- ∞→1️⃣ `ProblemStatement`
- ∞→1️⃣ `Solution`