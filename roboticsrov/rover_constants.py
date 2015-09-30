def generate_webcam_hook_string(object_name):
    return "startVideo=" + object_name + ".start,\nstopVideo=" + object_name + ".end,\n"

def generate_motor_hook_string(object_name):
    return "forward=" +\
       object_name + ".forward,\nreverse=" +\
       object_name + ".reverse,\nforwardLeft=" +\
       object_name + ".forwardLeft,\nforwardRight=" +\
       object_name + ".forwardRight,\nreverseLeft=" +\
       object_name + ".reverseLeft,\nreverseRight=" +\
       object_name + ".reverseRight,\nstop=" +\
       object_name + ".stop,\n"
