# Multi-Agent Interface System

Une interface flexible et extensible pour gérer plusieurs agents et déléguer des tâches.

## Architecture

```
AgentInterface (Interface utilisateur)
    ↓
TaskManager (Gestion des tâches)
    ↓
Agents (Exécution)
  ├─ FileAgent
  ├─ DataAgent
  ├─ ComputeAgent
  └─ Agents personnalisés
```

## Composants

### 1. **Agent** (classe abstraite)
La base pour tous les agents. Chaque agent doit implémenter:
- `can_handle(task_type)` - Vérifier si l'agent peut exécuter ce type de tâche
- `execute(task)` - Exécuter la tâche

### 2. **Agents prédéfinis**

#### FileAgent
Opérations sur les fichiers:
- `read` - Lire un fichier
- `write` - Écrire dans un fichier
- `delete` - Supprimer un fichier
- `list` - Lister les fichiers d'un répertoire

#### DataAgent
Traitement de données:
- `filter` - Filtrer les données
- `transform` - Transformer les données
- `aggregate` - Agréger les données

#### ComputeAgent
Tâches de calcul:
- `calculate` - Évaluer une expression mathématique

### 3. **TaskManager**
Gère:
- La file d'attente des tâches
- L'assignation des tâches aux agents
- L'exécution et le suivi des tâches
- Les statistiques d'exécution

### 4. **AgentInterface**
Interface utilisateur pour:
- Soumettre des tâches
- Exécuter les tâches
- Consulter le statut
- Obtenir les statistiques

## Utilisation

### Installation des dépendances
```bash
pip install graphifyy flask
```

### Usage simple

```python
from multi_agent_interface import AgentInterface

# Créer l'interface
interface = AgentInterface()

# Soumettre des tâches
task1 = interface.submit_task(
    name="Filter data",
    task_type="filter",
    params={
        "data": [1, 2, 3, 4, 5],
        "condition": lambda x: x > 2
    }
)

# Exécuter toutes les tâches
interface.execute_all()

# Afficher le statut
interface.print_status()
```

### Créer un agent personnalisé

```python
from multi_agent_interface import Agent, Task, TaskResult
import time

class EmailAgent(Agent):
    def __init__(self):
        super().__init__("EmailAgent", ["send_email"])
    
    def can_handle(self, task_type: str) -> bool:
        return task_type in self.capabilities
    
    def execute(self, task: Task) -> TaskResult:
        start = time.time()
        try:
            to = task.params.get("to")
            subject = task.params.get("subject")
            body = task.params.get("body")
            
            # Envoyer l'email (simulé ici)
            output = f"Email sent to {to}: {subject}"
            
            self.tasks_completed += 1
            return TaskResult(
                task_id=task.id,
                success=True,
                output=output,
                agent_name=self.name,
                execution_time=time.time() - start
            )
        except Exception as e:
            self.tasks_failed += 1
            return TaskResult(
                task_id=task.id,
                success=False,
                output=None,
                error=str(e),
                agent_name=self.name,
                execution_time=time.time() - start
            )

# Utiliser l'agent
interface.register_agent(EmailAgent())

task = interface.submit_task(
    name="Send welcome email",
    task_type="send_email",
    params={
        "to": "user@example.com",
        "subject": "Welcome",
        "body": "Welcome to our service!"
    }
)

interface.execute_task(task)
```

## API Web (Flask)

### Démarrer le serveur
```bash
python agent_web_interface.py
```

### Endpoints

#### Health Check
```
GET /api/health
```

#### Agents
```
GET /api/agents                    # Lister les agents
POST /api/agents/register          # Enregistrer un agent
```

#### Tâches
```
GET /api/tasks                     # Lister toutes les tâches
POST /api/tasks                    # Créer une nouvelle tâche
GET /api/tasks/<id>                # Obtenir une tâche
POST /api/tasks/<id>/execute       # Exécuter une tâche
POST /api/tasks/execute-all        # Exécuter toutes les tâches
POST /api/tasks/batch              # Créer plusieurs tâches
```

#### Statistiques
```
GET /api/statistics                # Statistiques d'exécution
GET /api/status                    # Statut complet du système
GET /api/dashboard                 # Données du tableau de bord
```

### Exemples de requêtes

#### Créer une tâche
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Filter numbers",
    "task_type": "filter",
    "params": {
      "data": [1, 2, 3, 4, 5],
      "condition": "lambda x: x > 2"
    }
  }'
```

#### Exécuter une tâche
```bash
curl -X POST http://localhost:5000/api/tasks/task_0/execute
```

#### Obtenir le statut
```bash
curl http://localhost:5000/api/status
```

## Exemples

Voir `agent_examples.py` pour des exemples complets:
```bash
python agent_examples.py
```

### Exemples inclus
1. **Basic Tasks** - Exécution de tâches simples
2. **Custom Agents** - Créer et utiliser des agents personnalisés
3. **Mixed Workload** - Mélanger différents types de tâches
4. **Priority Handling** - Gérer les priorités

## Caractéristiques

- ✅ **Multi-agent extensible** - Créer facilement de nouveaux agents
- ✅ **Gestion des tâches** - File d'attente, priorité, dépendances
- ✅ **Assignation intelligente** - Choisit le meilleur agent disponible
- ✅ **Suivi d'exécution** - Historique et statistiques
- ✅ **API REST** - Interface web complète
- ✅ **Agents prédéfinis** - FileAgent, DataAgent, ComputeAgent
- ✅ **Extensible** - Créer des agents personnalisés facilement

## Structure des tâches

```python
Task(
    id="task_0",
    name="Filter data",
    task_type="filter",           # Type de tâche
    priority=0,                    # 0 = normal, > 0 = plus important
    params={},                     # Paramètres spécifiques
    status=TaskStatus.PENDING,     # Statut actuel
    assigned_agent=None,           # Agent assigné
    dependencies=[],               # IDs des tâches dépendantes
)
```

## Status de tâches

- **PENDING** - En attente d'exécution
- **ASSIGNED** - Assignée à un agent
- **IN_PROGRESS** - En cours d'exécution
- **COMPLETED** - Complétée avec succès
- **FAILED** - Échouée
- **CANCELLED** - Annulée

## Performances

Le système peut gérer:
- ✓ Centaines de tâches simultanées
- ✓ Dizaines d'agents parallèles
- ✓ Exécution asynchrone (future amélioration)

## Amélirations futures

- [ ] Exécution asynchrone avec asyncio
- [ ] Persistance des tâches (base de données)
- [ ] Interface web complète (React/Vue)
- [ ] Gestion des dépendances entre tâches
- [ ] Load balancing avancé
- [ ] Retry automatique
- [ ] Métriques Prometheus
