from jinja2 import Template

def render_material_created_template(material_title: str, subject: str, created_by: str) -> str:
    """Render HTML email template for material created event"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #4CAF50; color: white; padding: 10px; text-align: center; }
            .content { padding: 20px; background-color: #f9f9f9; }
            .footer { margin-top: 20px; padding: 10px; text-align: center; color: #666; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Educational Center Notification</h2>
            </div>
            <div class="content">
                <h3>{{ subject }}</h3>
                <p>A new educational material has been added to the system:</p>
                <div style="background-color: white; padding: 15px; border-left: 4px solid #4CAF50; margin: 15px 0;">
                    <h4 style="margin-top: 0;">{{ material_title }}</h4>
                    <p><strong>Created by:</strong> {{ created_by }}</p>
                </div>
                <p>You can view this material in the educational portal.</p>
            </div>
            <div class="footer">
                <p>This is an automated notification from Educational Center System.</p>
                <p>Please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    template = Template(html_template)
    return template.render(
        material_title=material_title,
        subject=subject,
        created_by=created_by
    )

def render_simple_notification_template(subject: str, message: str) -> str:
    """Render simple HTML template"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #f9f9f9; padding: 20px; border-radius: 5px;">
            <h2 style="color: #4CAF50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">
                {{ subject }}
            </h2>
            <div style="padding: 15px; background-color: white; border-radius: 3px; margin: 15px 0;">
                {{ message|safe }}
            </div>
            <div style="margin-top: 20px; padding-top: 10px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                <p>Educational Center System • Automated Notification</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    template = Template(html_template)
    return template.render(subject=subject, message=message.replace('\n', '<br>'))