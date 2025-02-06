author_spec = {
    "openapi": "3.0.0",
    "info": {
        "title": "Authors API",
        "version": "1.0.0",
        "description": "API для управления авторами книг."
    },
    "paths": {
        "/api/authors": {
            "get": {
                "summary": "Retrieve a list of authors",
                "tags": [
                    "authors"
                ],
                "responses": {
                    "200": {
                        "description": "A list of authors",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Author"
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "No authors found",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "example": "No authors found"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Create a new author",
                "tags": [
                    "authors"
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "$ref": "#/components/schemas/Author"
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "The author has been created successfully",
                        "content": {
                            "application/json": {
                                "$ref": "#/components/schemas/Author"
                            }
                        }
                    },
                    "400": {
                        "description": "Validation error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "example": "Invalid input data"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/authors/{id}": {
            "get": {
                "summary": "Retrieve an author by ID",
                "tags": [
                    "authors"
                ],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "required": True,
                        "schema": {
                            "$ref": "#/components/schemas/Author/properties/id"
                        },
                        "description": "The ID of the author to retrieve."
                    }
                ],
                "responses": {
                    "200": {
                        "description": "A single author object.",
                        "content": {
                            "application/json": {
                                "$ref": "#/components/schemas/Author"
                            }
                        }
                    }
                },
                "404": {
                    "description": "Author not found.",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "Author not found"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "delete": {
                "summary": "Delete an author by their ID",
                "tags": [
                    "authors"
                ],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        },
                        "description": "The ID of the author to delete."
                    }
                ],
                "responses": {
                    "200": {
                        "description": "The author has been deleted successfully.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "example": "Author with id 1 has been deleted."
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Author not found.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "example": "Author not found"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "patch": {
                "summary": "Partially update an existing author by their ID",
                "tags": [
                    "authors"
                ],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "required": True,
                        "schema": {
                            "$ref": "#/components/schemas/Author/properties/id"
                        },
                        "description": "The ID of the author to update."
                    },
                    {
                        "in": "body",
                        "name": "author_updates",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "first_name": {
                                    "type": "string",
                                    "example": "John"
                                },
                                "last_name": {
                                    "type": "string",
                                    "example": "Doe"
                                },
                                "middle_name": {
                                    "type": "string",
                                    "example": ""
                                }
                            }
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "The author has been updated successfully.",
                        "content": {
                            "application/json": {
                                "$ref": "#/components/schemas/Author"
                            }
                        }
                    },
                    "404": {
                        "description": "Author not found.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "example": "Author not found"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Author": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "first_name": {
                        "type": "string"
                    },
                    "last_name": {
                        "type": "string"
                    },
                    "middle_name": {
                        "type": "string"
                    }
                },
                "required": [
                    "first_name",
                    "last_name"
                ]
            }
        }
    }
}
