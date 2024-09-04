"""
Database for the Friends.
"""

from django.db import models
from django.conf import settings


class FriendList(models.Model):
    """Model to store the list of the friends in users profile."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user",
    )
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="friends",
    )

    def __str__(self) -> str:
        return f"{self.user.username}'s Friend List"

    def add_friend(self, account):
        """Add a new friend."""
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        """Remove a friend."""
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        """Initiating the action of unfriending."""
        remover_friends_list = self

        remover_friends_list.remove_friend(removee)

        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_friend(self, friend):
        """Are we friend."""
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    """A model to store the sender and receiver."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        DECLINED = "declined", "Declined"
        CANCELLED = "cancelled", "Cancelled"

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sender",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="receiver",
    )
    is_active = models.BooleanField(default=True, blank=True, null=False)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}'s request to {self.receiver.username}"

    def accept(self):
        """
        Accept a friend request, update both sender and receiver
        friend lists.
        """
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.status = self.Status.ACCEPTED
                self.is_active = False
                self.save()

    def decline(self):
        """Decline a friend request."""
        self.status = self.Status.DECLINED
        self.is_active = False
        self.save()

    def cancel(self):
        """Cancel the send friend request."""
        self.status = self.Status.DECLINED
        self.is_active = False
        self.save()
