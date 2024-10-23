import os


from embedchain import App

app = App.from_config(config_path="config.yaml")
app.add("user-guide.pdf", data_type='pdf_file')
print(app.query("What are the safety reminders in the guide?"))
app.deploy()