from django.core.cache import cache
from .models import Property
import logging

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all().values('id', 'title', 'description', 'price', 'location', 'created_at'))
        cache.set('all_properties', properties, 3600)
    return properties


def get_redis_cache_metrics():
    from django_redis import get_redis_connection
    logger = logging.getLogger(__name__)
    try:
        conn = get_redis_connection("default")
        info = conn.info()
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_requests = hits + misses
        hit_ratio = (hits / total_requests) if total_requests > 0 else 0
        metrics = {
            'keyspace_hits': hits,
            'keyspace_misses': misses,
            'hit_ratio': hit_ratio
        }
        logger.info(f"Redis cache metrics: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {'error': str(e)}
