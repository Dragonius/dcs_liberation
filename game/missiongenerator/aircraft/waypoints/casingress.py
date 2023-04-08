import logging

from dcs.planes import (
    P_51D,
    P_51D_30_NA,
    P_47D_30,
    P_47D_30bl1,
    P_47D_40,
    A_20G,
    MosquitoFBMkVI,
    SpitfireLFMkIX,
    SpitfireLFMkIXCW,
    FW_190A8,
    FW_190D9,
    Bf_109K_4,
    I_16,
)
from dcs.point import MovingPoint
from dcs.task import EngageTargets, EngageTargetsInZone, Targets

from game.ato.flightplans.cas import CasFlightPlan
from game.utils import nautical_miles
from .pydcswaypointbuilder import PydcsWaypointBuilder


class CasIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        if isinstance(self.flight.flight_plan, CasFlightPlan):
            waypoint.add_task(
                EngageTargetsInZone(
                    position=self.flight.flight_plan.layout.target.position,
                    radius=int(self.flight.flight_plan.engagement_distance.meters),
                    targets=[
                        Targets.All.GroundUnits.GroundVehicles,
                        Targets.All.GroundUnits.AirDefence.AAA,
                        Targets.All.GroundUnits.Infantry,
                    ],
                )
            )
        else:
            logging.error("No CAS waypoint found. Falling back to search and engage")
            waypoint.add_task(
                EngageTargets(
                    max_distance=int(nautical_miles(10).meters),
                    targets=[
                        Targets.All.GroundUnits.GroundVehicles,
                        Targets.All.GroundUnits.AirDefence.AAA,
                        Targets.All.GroundUnits.Infantry,
                    ],
                )
            )

        # Decrease the waypoint altitude in order to increase the chances that the AI
        # is able to spot the targets on the ground
        # Divide by three for warbirds, by two for everything else
        if self.group.units[0].unit_type in [
            P_51D,
            P_51D_30_NA,
            P_47D_30,
            P_47D_30bl1,
            P_47D_40,
            A_20G,
            MosquitoFBMkVI,
            SpitfireLFMkIX,
            SpitfireLFMkIXCW,
            FW_190A8,
            FW_190D9,
            Bf_109K_4,
            I_16,
        ]:
            waypoint.alt = waypoint.alt / 3
        else:
            #    waypoint.alt = waypoint.alt / 2
            waypoint.alt = waypoint.alt
