#
#    Copyright (c) 2022 Project CHIP Authors
#    All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

import logging

import chip.clusters as Clusters
from chip.interaction_model import Status
from matter_testing_support import MatterBaseTest, TestStep, async_test_body, default_matter_test_main
from mobly import asserts


class TC_ECAL_25(MatterBaseTest):
    async def read_ecal_attribute_expect_success(self, endpoint, attribute):
        cluster = Clusters.Objects.EnergyCalendar
        return await self.read_single_attribute_check_success(dev_ctrl=self.default_controller,
                                                              node_id=self.dut_node_id,
                                                              endpoint=endpoint,
                                                              cluster=cluster,
                                                              attribute=attribute)

    async def read_ecal_calendar_id(self, endpoint=0):
        return await self.read_ecal_attribute_expect_success(endpoint, Clusters.EnergyCalendar.Attributes.CalendarID)

    async def write_ecal_calendar_id(self, calendar_id, endpoint=0):
        # This returns an attribute status
        result = await self.default_controller.WriteAttribute(self.dut_node_id, [(endpoint, Clusters.EnergyCalendar.Attributes.CalendarID(calendar_id))])
        asserts.assert_equal(result[0].Status, Status.Success, "CalendarID write failed")

    def desc_TC_ECAL_25(self) -> str:
        """Returns a description of this test"""
        return "[TC-ECAL-25] CalendarID: valid value"

    def steps_TC_ECAL_25(self) -> list[TestStep]:
        steps = [TestStep(1, "Commissioning, already done", is_commissioning=True),
                 TestStep(2, "Set the attribute value to 0"),
                 TestStep(3, "Read the attribute value"),
                 TestStep(4, "Set the attribute value to 2147483648"),
                 TestStep(5, "Read the attribute value"),
                 TestStep(6, "Set the attribute value to 4294967294"),
                 TestStep(7, "Read the attribute value"),
                 TestStep(8, "Set the attribute value to 4294967295 (NULL)"),
                 TestStep(9, "Read the attribute value")
                 ]
        return steps

    @async_test_body
    async def test_TC_ECAL_25(self):
        self.step(1)  # commissioning

        self.step(2)
        await self.write_ecal_calendar_id(0)

        self.step(3)
        await self.read_ecal_calendar_id()

        self.step(4)
        await self.write_ecal_calendar_id(2147483648)

        self.step(5)
        await self.read_ecal_calendar_id()

        self.step(6)
        await self.write_ecal_calendar_id(4294967294)

        self.step(7)
        await self.read_ecal_calendar_id()

        self.step(8)
        await self.write_ecal_calendar_id(4294967295)

        self.step(9)
        await self.read_ecal_calendar_id()


if __name__ == "__main__":
    default_matter_test_main()
