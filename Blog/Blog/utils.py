from django.utils.text import slugify


def unique_slug_generator(model_instance, title, slug_field):
    slug = slugify(title)
    model_class = model_instance.__class__  # return the name of the class

    # check if slug exist, if it does then add an increment pk to make it unique
    while model_class._default_manager.filter(slug=slug).exists():
        # model_class.default_manager.filter <=> Post.objects.filter
        object_pk = model_class._default_manager.latest(
            'pk')  # return latest created object
        # take the returned object, find its pk and increment by 1, return integer pk
        object_pk = object_pk.pk + 1

        slug = f'{slug}-{object_pk}'

    return slug
