from __future__ import annotations

from typing import Type

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .waypointbuilder import WaypointBuilder
from .. import FlightWaypoint
from ..flightwaypointtype import FlightWaypointType
from ...theater import FrontLine


class EscortFlightPlan(FormationAttackFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder


class Builder(FormationAttackBuilder[EscortFlightPlan, FormationAttackLayout]):
    def layout(self) -> FormationAttackLayout:
        assert self.package.waypoints is not None

        location = self.package.target
        builder = WaypointBuilder(self.flight, self.coalition)
        if isinstance(location, FrontLine):
            from game.missiongenerator.frontlineconflictdescription import (
                FrontLineConflictDescription,
            )

            (
                ingress_point,
                heading,
                distance,
            ) = FrontLineConflictDescription.frontline_vector(
                location, self.theater, self.coalition.game.settings
            )
            target_point = ingress_point.point_from_heading(
                heading.degrees, distance / 2
            )
            egress_point = ingress_point.point_from_heading(heading.degrees, distance)

            ingress_distance = ingress_point.distance_to_point(
                self.flight.departure.position
            )
            egress_distance = egress_point.distance_to_point(
                self.flight.departure.position
            )
            if egress_distance < ingress_distance:
                ingress_point, egress_point = egress_point, ingress_point

            ingress = builder.ingress(
                FlightWaypointType.INGRESS_ESCORT, ingress_point, location
            )
            target = FlightWaypoint(
                self.package.target.name,
                FlightWaypointType.TARGET_POINT,
                target_point,
                self.doctrine.ingress_altitude * 0.5,
                description=self.package.target.name,
                pretty_name=self.package.target.name,
            )
            # egress = builder.egress(egress_point, location)
            split = builder.split(egress_point)
        else:

            ingress, target = builder.escort(
                self.package.waypoints.ingress, self.package.target
            )
            split = builder.split(self.package.waypoints.split)

        hold = builder.hold(self._hold_point())
        join = builder.join(self.package.waypoints.join)
        refuel = builder.refuel(self.package.waypoints.refuel)

        return FormationAttackLayout(
            departure=builder.takeoff(self.flight.departure),
            hold=hold,
            nav_to=builder.nav_path(
                hold.position, join.position, self.doctrine.ingress_altitude
            ),
            join=join,
            ingress=ingress,
            targets=[target],
            split=split,
            refuel=refuel,
            nav_from=builder.nav_path(
                refuel.position,
                self.flight.arrival.position,
                self.doctrine.ingress_altitude,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self) -> EscortFlightPlan:
        return EscortFlightPlan(self.flight, self.layout())
