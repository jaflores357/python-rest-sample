import os
from locust import HttpLocust, TaskSet, TaskSequence, between, seq_task

class LoadSequence(TaskSequence):
    @seq_task(1)
    def load_healthcheck_get(self):
        self.client.get("/healthcheck")

    @seq_task(2)
    def load_list_machines_elb(self):
        self.client.get("/elb/default-elb")

    @seq_task(3)
    def load_elb_elb_name_delete(self):
        machine_id = os.environ.get("LOCUST_MACHINEID")
        self.client.delete("/elb/default-elb", json={"instanceId": machine_id})

    @seq_task(4)
    def load_attach_instance(self):
        machine_id = os.environ.get("LOCUST_MACHINEID")
        self.client.post("/elb/default-elb", json={"instanceId": machine_id})

class UserBehavior(TaskSet):
    tasks = {LoadSequence:1}

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(2, 5)

