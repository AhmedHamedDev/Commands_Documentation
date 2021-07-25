# Django Built-in Signals

    # django.db.models.signals.pre_init:
    # receiver_function(sender, *args, **kwargs)

    # django.db.models.signals.post_init:
    # receiver_function(sender, instance)

    # django.db.models.signals.pre_save:
    # receiver_function(sender, instance, raw, using, update_fields)

    # django.db.models.signals.post_save:
    # receiver_function(sender, instance, created, raw, using, update_fields)

    # django.db.models.signals.pre_delete:
    # receiver_function(sender, instance, using)

    # django.db.models.signals.post_delete:
    # receiver_function(sender, instance, using)

    # django.db.models.signals.m2m_changed:
    # receiver_function(sender, instance, action, reverse, model, pk_set, using)

# Request/Response Signals

    # django.core.signals.request_started:
    # receiver_function(sender, environ)

    # django.core.signals.request_finished:
    # receiver_function(sender, environ)

    # django.core.signals.got_request_exception:
    # receiver_function(sender, request)


from django.db.models.signals import pre_save

def blog_pre_save_function(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = f"{instance.title}-{instance.id}"
        

pre_save.connect(blog_pre_save_function, sender=Blog)