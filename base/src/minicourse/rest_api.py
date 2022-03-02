import enum
from src.commons import entities
from singleton_injector import injector
from src.commons.http import HttpMethods
from src.minicourse import stack as minicourse_stack, lambdas as minicourse_lambdas
from src.commons import security


class Scopes(enum.Enum):
    W_MINICOURSE = "w_minicourse"
    R_MINICOURSE = "r_minicourse"
    W_CATEGORY = "w_category"
    R_CATEGORY = "r_category"


@injector
class MinicourseRestApi(entities.LambdaRestApi):
    def __init__(
        self,
        scope: minicourse_stack.MinicourseStack,
        create_minicourse: minicourse_lambdas.CreateMinicourseLambda,
        get_minicourse: minicourse_lambdas.GetMinicourseLambda,
        update_minicourse: minicourse_lambdas.UpdateMinicourseLambda,
        create_category: minicourse_lambdas.CreateCategoryLamdba,
        get_category: minicourse_lambdas.GetCategoriesLambda,
        delete_category: minicourse_lambdas.DeleteCategoryLambda,
        delete_minicourse: minicourse_lambdas.DeleteMinicourseLambda,
        update_category: minicourse_lambdas.UpdateCategoryLambda,
    ):
        api_id = "MinicourseRestApi"

        super().__init__(
            scope=scope,
            id=api_id,
            name=api_id,
            authorizer=security.Auth0Authorizer(scope, api_id),
        )

        self.main_resource = self.root.add_resource("minicourse")

        self.add_method(
            self.main_resource,
            method=HttpMethods.POST,
            integration_lambda=create_minicourse,
            roles=[Scopes.W_MINICOURSE, Scopes.R_CATEGORY],
        )

        self.get_minicourse = self.main_resource.add_resource("get")

        self.add_method(
            self.get_minicourse,
            method=HttpMethods.POST,
            integration_lambda=get_minicourse,
            roles=[Scopes.R_MINICOURSE, Scopes.R_CATEGORY],
        )

        self.add_method(
            self.main_resource,
            method=HttpMethods.PUT,
            integration_lambda=update_minicourse,
            roles=[Scopes.R_MINICOURSE, Scopes.R_CATEGORY],
        )

        self.category_resource = self.main_resource.add_resource("category")

        self.add_method(
            self.category_resource,
            method=HttpMethods.POST,
            integration_lambda=create_category,
            roles=[Scopes.W_CATEGORY],
        )

        self.get_categories = self.category_resource.add_resource("get")

        self.add_method(
            self.get_categories,
            method=HttpMethods.POST,
            integration_lambda=get_category,
            roles=[Scopes.R_CATEGORY],
        )

        self.add_method(
            self.category_resource,
            method=HttpMethods.DELETE,
            integration_lambda=delete_category,
            roles=[Scopes.W_CATEGORY],
        )

        self.add_method(
            self.main_resource,
            method=HttpMethods.DELETE,
            integration_lambda=delete_minicourse,
            roles=[Scopes.W_MINICOURSE, Scopes.R_MINICOURSE],
        )

        self.add_method(
            self.category_resource,
            method=HttpMethods.PUT,
            integration_lambda=update_category,
            roles=[Scopes.W_CATEGORY, Scopes.R_CATEGORY],
        )

        self.authorizer.construct_roles()
