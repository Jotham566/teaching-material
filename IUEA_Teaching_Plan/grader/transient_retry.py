"""One bounded retry for transport timeouts, never for a grading decision."""
from urllib.error import URLError

def run(operation):
    timeouts=[]
    for attempt in (1,2):
        try:
            result=operation()
        except (TimeoutError,URLError) as exc:
            if isinstance(exc,URLError) and not isinstance(exc.reason,TimeoutError):raise
            timeouts.append(str(exc)[:200])
            if attempt==2:
                raise TimeoutError('Local inference timed out on both attempts; no mark was produced.') from exc
        else:
            result['inference_attempts']=attempt
            if timeouts:result['prior_transport_timeouts']=timeouts
            return result
