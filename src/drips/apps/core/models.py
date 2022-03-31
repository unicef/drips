from unicef_auth.models import AbstractUNICEFUser


class User(AbstractUNICEFUser):

    class Meta(AbstractUNICEFUser.Meta):
        app_label = 'core'
