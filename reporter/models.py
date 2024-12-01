from django.db import models

# Create your models here.
class Report(models.Model):
    # Types of reports as choices
    REPORT_TYPE_CHOICES = [
        ('pothole', 'Pothole'),
        ('speed_breaker', 'Unmarked Speed-breaker'),
        ('standing_water', 'Standing Water'),
    ]


    # auto_now_add=True tells django to automatically set this attribute to the
    # current date and time whenever the user creates a new report

    # Fields for the model
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    report_description = models.CharField(max_length=200)
    location_lat = models.FloatField(help_text="Latitude of the issue location")
    location_lon = models.FloatField(help_text="Longitude of the issue location")
    reported_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the report was created")
    is_resolved = models.BooleanField(default=False, help_text="Status of the report: Resolved or Not")
    image = models.ImageField(default='fallback.png', blank=True, help_text="Upload an image of the issue")
    priority = models.IntegerField(default=1, choices=[(i, str(i)) for i in range(1, 11)], help_text="Priority of the report (1-10)")

    class Meta:
        verbose_name_plural = 'Reports'

    def __str__(self):
        return f"{self.get_report_type_display()} at ({self.location_lat}, {self.location_lon})"


