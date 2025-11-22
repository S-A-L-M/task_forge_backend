from datetime import datetime
from typing import List, Optional

class Node:
    """
    Representa un nodo en el árbol (puede ser tarea o proyecto)
    """
    nodes = []  # Base de datos en memoria (simple para MVP)
    next_id = 1
    
    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        due_date: str = None,
        priority: str = 'medium',
        tags: List[str] = None,
        notes: Optional[str] = None,
        parent_id: Optional[str] = None,
        is_project: bool = False,
        is_completed: bool = False,
        node_id: Optional[str] = None
    ):
        self.id = node_id if node_id else str(Node.next_id)
        if not node_id:
            Node.next_id += 1
            
        self.title = title
        self.description = description
        self.due_date = due_date or datetime.now().isoformat()
        self.priority = priority
        self.tags = tags or []
        self.notes = notes
        self.parent_id = parent_id
        self.is_project = is_project
        self.is_completed = is_completed
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self):
        """Convierte el nodo a diccionario para JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'priority': self.priority,
            'tags': self.tags,
            'notes': self.notes,
            'parent_id': self.parent_id,
            'is_project': self.is_project,
            'is_completed': self.is_completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Crea un nodo desde un diccionario"""
        return Node(
            node_id=data.get('id'),
            title=data['title'],
            description=data.get('description'),
            due_date=data.get('due_date'),
            priority=data.get('priority', 'medium'),
            tags=data.get('tags', []),
            notes=data.get('notes'),
            parent_id=data.get('parent_id'),
            is_project=data.get('is_project', False),
            is_completed=data.get('is_completed', False)
        )
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los nodos"""
        return [node.to_dict() for node in cls.nodes]
    
    @classmethod
    def get_by_id(cls, node_id: str):
        """Obtiene un nodo por ID"""
        for node in cls.nodes:
            if node.id == node_id:
                return node
        return None
    
    @classmethod
    def create(cls, data: dict):
        """Crea un nuevo nodo"""
        node = cls.from_dict(data)
        cls.nodes.append(node)
        return node
    
    @classmethod
    def update(cls, node_id: str, data: dict):
        """Actualiza un nodo existente"""
        node = cls.get_by_id(node_id)
        if node:
            node.title = data.get('title', node.title)
            node.description = data.get('description', node.description)
            node.due_date = data.get('due_date', node.due_date)
            node.priority = data.get('priority', node.priority)
            node.tags = data.get('tags', node.tags)
            node.notes = data.get('notes', node.notes)
            node.parent_id = data.get('parent_id', node.parent_id)
            node.is_project = data.get('is_project', node.is_project)
            node.is_completed = data.get('is_completed', node.is_completed)
            node.updated_at = datetime.now().isoformat()
            return node
        return None
    
    @classmethod
    def delete(cls, node_id: str):
        """Elimina un nodo y sus hijos"""
        # Eliminar hijos recursivamente
        children = [n for n in cls.nodes if n.parent_id == node_id]
        for child in children:
            cls.delete(child.id)
        
        # Eliminar el nodo
        cls.nodes = [n for n in cls.nodes if n.id != node_id]
        return True
    
    @classmethod
    def search(cls, query: str):
        """Busca nodos por título, descripción o tags"""
        query_lower = query.lower()
        results = []
        
        for node in cls.nodes:
            if (query_lower in node.title.lower() or
                (node.description and query_lower in node.description.lower()) or
                any(query_lower in tag.lower() for tag in node.tags)):
                results.append(node.to_dict())
        
        return results