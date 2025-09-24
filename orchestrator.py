"""Planning-enabled orchestrator for the FlexibleBusinessChat system."""

from typing import Callable, Sequence

from crewai import Crew, Process

from config import get_llm
from tasks.dynamic_tasks import create_dispatcher_task


class PlanningOrchestrator:
    """Coordinate specialized agents through a hierarchical planning crew."""

    def __init__(
        self,
        dispatcher_factory: Callable[[], object],
        crew_cls: type[Crew] = Crew,
        llm_provider: Callable[..., object] = get_llm,
    ) -> None:
        self._dispatcher_factory = dispatcher_factory
        self._crew_cls = crew_cls
        self._llm_provider = llm_provider

    def dispatch(
        self,
        user_request: str,
        agents: Sequence[object],
        context: dict,
    ):
        """Run the planning workflow and return the orchestrator's response."""

        dispatcher = self._dispatcher_factory()
        dispatcher_task = create_dispatcher_task(
            dispatcher=dispatcher,
            user_request=user_request,
            available_agents=list(agents),
            context=context,
        )

        manager_llm = self._llm_provider()
        planning_llm = manager_llm

        crew = self._crew_cls(
            agents=[dispatcher, *agents],
            tasks=[dispatcher_task],
            process=Process.hierarchical,
            manager_llm=manager_llm,
            planning=True,
            planning_llm=planning_llm,
            verbose=True,
            memory=True,
            full_output=True,
        )

        return crew.kickoff()


__all__ = ["PlanningOrchestrator"]
