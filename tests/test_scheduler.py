import pytest
from unittest.mock import MagicMock, patch

def test_scheduler_setup():
    # We will implement scheduler.py later. TDD approach.
    # We assume there is a function setup_scheduler() in scheduler.py
    from scheduler import setup_scheduler
    
    # Mock AsyncIOScheduler
    with patch("scheduler.AsyncIOScheduler") as mock_scheduler_class:
        mock_scheduler = mock_scheduler_class.return_value
        
        setup_scheduler()
        
        # Verify scheduler is initialized and started
        mock_scheduler_class.assert_called_once()
        mock_scheduler.start.assert_called_once()
        
        # Verify job is added for morning brief
        mock_scheduler.add_job.assert_called()
        
        # Check if morning brief job is scheduled
        calls = mock_scheduler.add_job.call_args_list
        morning_brief_scheduled = any(
            kwargs.get("id") == "morning_brief" or "morning" in str(args)
            for args, kwargs in calls
        )
        assert morning_brief_scheduled, "Morning brief job should be scheduled"
