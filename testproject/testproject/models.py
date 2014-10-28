from django.db import models
from django.db.models.signals import post_save, post_delete

from mptt.models import TreeManager

from groups_manager.models import Group, GroupType, group_save, group_delete


class Legion(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (('view_legion', 'View Legion'), )

    def __unicode__(self):
        return self.name


class ProjectManager(TreeManager):

    def all(self, *args, **kwargs):
        queryset = super(ProjectManager, self).all(*args, **kwargs)
        return queryset.filter(group_type__codename='project')

    def filter(self, *args, **kwargs):
        queryset = super(ProjectManager, self).filter(*args, **kwargs)
        return queryset.filter(group_type__codename='project')


class Project(Group):
    objects = ProjectManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.group_type:
            self.group_type = GroupType.objects.get_or_create(label='Project')[0]
        super(Project, self).save(*args, **kwargs)

post_save.connect(group_save, sender=Project)
post_delete.connect(group_delete, sender=Project)


class WorkGroupManager(TreeManager):

    def all(self, *args, **kwargs):
        queryset = super(WorkGroupManager, self).all(*args, **kwargs)
        return queryset.filter(group_type__codename='workgroup')

    def filter(self, *args, **kwargs):
        queryset = super(WorkGroupManager, self).filter(*args, **kwargs)
        return queryset.filter(group_type__codename='workgroup')


class WorkGroup(Group):
    objects = WorkGroupManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.group_type:
            self.group_type = GroupType.objects.get_or_create(label='Workgroup')[0]
        super(WorkGroup, self).save(*args, **kwargs)

post_save.connect(group_save, sender=WorkGroup)
post_delete.connect(group_delete, sender=WorkGroup)


class Pipeline(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (('view_pipeline', 'View Pipeline'), )
