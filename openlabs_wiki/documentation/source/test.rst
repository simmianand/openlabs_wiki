Home Page
------------
**These are the Login Page contents:**
i) Register the new user.
ii) Login register user only.


Register New User
======================

Registration is quick and easy. It enables you to enjoy benefits of registration such as creating wiki pages, updating wiki pages , setting up pages to public and private, comparing user generated wiki pages, reverting back to your previous page, auto login and exclusive content. To start taking advantage of these benefits click register.

.. image:: _images/login.png
   :align: center
   :width: 500
   :height: 400


Using the Django authentication system
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

The project uses the Django’s authentication system in its default configuration. This configuration has evolved to serve the most common project needs, handling a reasonably wide range of tasks, and has a careful implementation of passwords and permissions, and can handle many projects.

Django authentication provides both authentication and authorization, together.User objects are the core of the authentication system.


Logins Registered User
======================

The **LOGIN** displays to users when portal direct entry is set in the urls.py file in the openlabs_wiki project. The text will appear in the module along with the fields for entering a User Name and Password and to registered user only and grant the privileges to the user to enter into the session where he can do the creating wiki pages, updating wiki pages , setting up pages to public and private, comparing user generated wiki pages, reverting back to your previous page.

.. image:: _images/login.png
   :align: center
   :width: 500
   :height: 400

Logout Page
===========

.. image:: _images/after_register.png
   :align: center
   :width: 500
   :height: 400
User will be having this kind of window. Then the user is logged out of
the session.

.. image:: _images/logout.png
   :align: center
   :width: 500
   :height: 400

Sets Wiki Page Public/Private
-----------------------------
If user wants to simply add his pages publically so that any body can see.
He can display them as public else private for not showing to the others.
By this functionality he will be able to provide both features to the
user.

.. image:: _images/private.png
   :align: center
   :width: 500
   :height: 400

