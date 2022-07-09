# import logging
# import os
#
# from office365.runtime.auth.client_credential import ClientCredential
# from office365.runtime.auth.user_credential import UserCredential
# from office365.sharepoint.client_context import ClientContext
# from office365.sharepoint.files.creation_information import FileCreationInformation
# from office365.sharepoint.files.file import File
# from office365.sharepoint.search.search_service import SearchService
#
# from sharepoint_rest_api import config
# from sharepoint_rest_api.builders.camlquery_builder import CamlQueryBuilder
# from sharepoint_rest_api.builders.querystring_builder import QueryStringBuilder
# from sharepoint_rest_api.builders.search_request_builder import SearchRequestBuilder
# from sharepoint_rest_api.config import SHAREPOINT_PAGE_SIZE
#
# logger = logging.getLogger(__name__)
#
#
# default_select = ['*', 'FileLeafRef']
#
#
# class SharePointClientException(BaseException):
#     """SharePoint Exception when initializing the client"""
#
#
# class SharePointClient:
#     """Client to access SharePoint Document Library"""
#
#     def __init__(self, *args, **kwargs) -> None:
#         self.relative_url = kwargs.get('relative_url', None)
#         self.site_path = kwargs.get('url', config.SHAREPOINT_TENANT)
#         if config.SHAREPOINT_CONNECTION == 'app':
#             client_id = kwargs.get('client_id', config.SHAREPOINT_CLIENT_ID)
#             client_secret = kwargs.get('client_secret', config.SHAREPOINT_CLIENT_SECRET)
#             credentials = ClientCredential(client_id, client_secret)
#         elif config.SHAREPOINT_CONNECTION == 'user':
#             username = kwargs.get('username', config.SHAREPOINT_USERNAME)
#             password = kwargs.get('password', config.SHAREPOINT_PASSWORD)
#             credentials = UserCredential(username, password)
#         else:
#             raise SharePointClientException('Invalid connection type')
#         self.folder = kwargs.get('folder', 'Documents')
#         self.context = ClientContext(self.site_path).with_credentials(credentials)
#
#     def __reduce__(self):
#         return SharePointClient, (self.relative_url, self.site_path, self.folder, )
#
#     def get_folder(self, folder_name):
#         """
#         :param folder_name: name of the folder
#         :return: folder object
#
#         Return folder object
#         """
#         list_obj = self.context.web.lists.get_by_title(folder_name)
#         folder = list_obj.root_folder
#         self.context.load(folder)
#         self.context.execute_query()
#         logger.info(f'List url: {folder.properties["ServerRelativeUrl"]}')
#         return folder
#
#     def read_folders(self, folder_name):
#         """
#         :param folder_name:
#         :return: folders
#
#         Return folders metadata for subfolder of current folder
#         """
#         self.get_folder(folder_name)
#         folders = self.context.web.folders
#         self.context.load(folders)
#         self.context.execute_query()
#         for folder in folders:
#             logger.info(f'Folder name: {folder.properties["Name"]}')
#         return folders
#
#     def read_items(self, filters=None, select=None):
#         """
#         :param filters: filter dictionary
#         :param scope: SharePoint scope
#         :return: items
#
#         Retrieves (filtered) items on current folder using querystring
#         """
#         filters = filters or dict()
#         querystring = QueryStringBuilder(filters).get_querystring()
#         list_object = self.context.web.lists.get_by_title(self.folder)
#         select_string = select or default_select
#         items = list_object.get_items().filter(querystring).select(select_string)
#         self.context.load(items)
#         self.context.execute_query()
#         return items
#
#     def read_file(self, filename):
#         """
#         :param filename: filename
#         :return:
#
#         Retrieve file in current folder
#         """
#         folder = self.get_folder(self.folder)
#         cur_file = folder.files.get_by_url(f'/{self.relative_url}/{self.folder}/{filename}')
#         self.context.load(cur_file)
#         self.context.execute_query()
#         logger.info(f'File name: {cur_file.properties["Name"]}')
#         return cur_file
#
#     def read_caml_items(self, filters=None, scope=None):
#         """
#         :param filters: filter dictionary
#         :param scope: SharePoint scope
#         :return: items
#
#         Retrieves (filtered) items on current folder using CamlQueries
#         """
#         filters = filters or dict()
#         list_obj = self.context.web.lists.get_by_title(self.folder)
#         qry = CamlQueryBuilder(filters, scope).get_query()
#         items = list_obj.get_items(qry)
#         self.context.execute_query()
#         return items
